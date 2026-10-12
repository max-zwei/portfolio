#!/usr/bin/env python3
"""Run one Codex app build and capture its emitted trace; standard library only."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import signal
import subprocess
import sys
import time
import uuid

MODEL = "gpt-6.1-sol"
EFFORT = "medium"
HERE = Path(__file__).resolve().parent
SKIP_DIRS = {".git", "node_modules", ".expo", ".npm-cache", ".cache", "dist", "build"}
INITIAL_IGNORE = "node_modules/\n.expo/\n.npm-cache/\n.cache/\ndist/\nbuild/\nartifacts/\n.env\n.env.*\n!.env.example\n"


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def checked_count(value):
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def validate_model_catalog(catalog, model=MODEL, effort=EFFORT):
    """Check cached metadata only; this is not a live access or billing check."""
    models = catalog.get("models", []) if isinstance(catalog, dict) else []
    if not isinstance(models, list):
        raise ValueError("The local Codex model catalog is malformed. Refresh it in Codex.")
    visible = [m for m in models if isinstance(m, dict) and m.get("visibility") == "list"]
    selected = next((m for m in visible if m.get("slug") == model), None)
    if selected is None:
        available = ", ".join(str(m.get("slug")) for m in visible) or "none listed"
        raise ValueError(f"Fixed model {model!r} is absent from the local Codex model catalog. "
                         f"Available entries: {available}. Refresh the catalog in Codex; "
                         "do not silently substitute another model in this experiment.")
    levels = selected.get("supported_reasoning_levels", [])
    efforts = [level.get("effort") for level in levels if isinstance(level, dict)]
    if effort not in efforts:
        raise ValueError(f"The local catalog does not list {effort!r} effort for {model!r}.")
    # Copy only model metadata, never the catalog's account identity or auth data.
    return {"check": "local_cached_catalog_only", "model": model,
            "display_name": selected.get("display_name"), "reasoning_effort": effort,
            "catalog_fetched_at": catalog.get("fetched_at"),
            "catalog_client_version": catalog.get("client_version"),
            "live_model_access_verified": False}


def load_model_preflight():
    path = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "models_cache.json"
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ValueError("Cannot read the local Codex model catalog. Open Codex, sign in, "
                         "and open its model picker to refresh the catalog before retrying.") from None
    return validate_model_catalog(catalog)


def error_message(event):
    """Extract human-readable errors, including JSON nested inside a message."""
    kind = event.get("type")
    if kind == "error":
        value = event.get("message", event.get("error", "Unspecified Codex error"))
    elif kind == "turn.failed":
        value = event.get("error", "Codex turn failed")
    elif kind == "item.completed" and isinstance(event.get("item"), dict) and event["item"].get("type") == "error":
        value = event["item"].get("message", "Unspecified Codex item error")
    else:
        return None
    for _ in range(8):
        if isinstance(value, dict):
            value = value.get("message", value.get("error", json.dumps(value)))
        elif isinstance(value, str):
            try:
                parsed = json.loads(value)
            except ValueError:
                return value
            if not isinstance(parsed, (dict, str)) or parsed == value:
                return value
            value = parsed
        else:
            return str(value)
    return str(value)


def summarize_usage(events, invalid_lines=0):
    """Only turn.completed usage; never sum streamed/cumulative item updates."""
    completions = [e for e in events if isinstance(e, dict) and e.get("type") == "turn.completed"]
    failures = [e for e in events if isinstance(e, dict) and e.get("type") in {"turn.failed", "error"}]
    records = []
    for event in completions:
        usage = event.get("usage")
        if not isinstance(usage, dict):
            records.append({"raw": usage, "input_tokens": None, "cached_input_tokens": None,
                            "output_tokens": None, "reasoning_output_tokens": None})
            continue
        cached = usage.get("cached_input_tokens")
        if cached is None and isinstance(usage.get("input_tokens_details"), dict):
            cached = usage["input_tokens_details"].get("cached_tokens")
        reasoning = usage.get("reasoning_output_tokens")
        if reasoning is None and isinstance(usage.get("output_tokens_details"), dict):
            reasoning = usage["output_tokens_details"].get("reasoning_tokens")
        records.append({"raw": usage, "input_tokens": checked_count(usage.get("input_tokens")),
                        "cached_input_tokens": checked_count(cached),
                        "output_tokens": checked_count(usage.get("output_tokens")),
                        "reasoning_output_tokens": checked_count(reasoning)})
    keys = ["input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens"]
    totals = {key: sum(r[key] for r in records) if records and all(r[key] is not None for r in records)
              else None for key in keys}
    inp, out, cached = totals["input_tokens"], totals["output_tokens"], totals["cached_input_tokens"]
    totals["input_plus_output_tokens"] = inp + out if inp is not None and out is not None else None
    totals["uncached_input_tokens_derived"] = inp - cached if inp is not None and cached is not None and inp >= cached else None
    complete = bool(records) and not failures and not invalid_lines and inp is not None and out is not None
    return {"status": "reported_totals_available" if complete else "incomplete_or_unavailable",
            "completed_turns": len(completions), "error_or_failed_turn_events": len(failures),
            "non_json_lines": invalid_lines, "reported_totals": totals,
            "per_completed_turn": records,
            "notes": [
                "Only usage on turn.completed events is aggregated. Raw fields are preserved.",
                "Cached input is a subset of input; it is not added again.",
                "Reasoning output is reported separately when available and is not added again to output.",
                "Missing counters are null, never estimated or silently replaced with zero.",
                "Interrupted/failed runs may omit usage. Reported usage is not an independent billing audit.",
                "Input/output totals describe token activity, not electricity or water consumption."]}


def readable(value, indent=0):
    prefix = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(prefix + str(key) + ":")
                lines.extend(readable(item, indent + 2))
            elif isinstance(item, str) and "\n" in item:
                lines.append(prefix + str(key) + ":")
                lines.extend(prefix + "  " + line for line in item.splitlines())
            else:
                lines.append(prefix + str(key) + ": " + str(item))
        return lines
    if isinstance(value, list):
        lines = []
        for index, item in enumerate(value):
            lines.append(prefix + f"[{index}]")
            lines.extend(readable(item, indent + 2))
        return lines
    return [prefix + str(value)]


def command_for(codex, app, capture):
    return [codex, "--ask-for-approval", "never", "exec", "--ignore-user-config",
            "--model", MODEL, "--config", f'model_reasoning_effort="{EFFORT}"',
            "--config", 'model_reasoning_summary="auto"',
            "--config", "hide_agent_reasoning=false",
            "--config", "features.multi_agent=false",
            "--config", "features.memories=false",
            "--config", "sandbox_workspace_write.network_access=true",
            "--sandbox", "workspace-write", "--cd", str(app), "--color", "never", "--json",
            "--output-last-message", str(capture / "final-message.txt"), "-"]


def version_of(command):
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=15)
        return {"command": command, "exit_code": result.returncode,
                "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"command": command, "error": str(exc)}


def stop_process(proc):
    if proc.poll() is not None:
        return
    os.killpg(proc.pid, signal.SIGINT)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()


def snapshot(app, capture):
    manifest = []
    for directory, dirs, files in os.walk(app, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(directory) / d).is_symlink())
        for name in sorted(files):
            path = Path(directory) / name
            if path.is_symlink() or name == ".env" or (name.startswith(".env.") and name != ".env.example"):
                continue
            try:
                digest = hashlib.sha256()
                with path.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        digest.update(chunk)
                manifest.append({"path": str(path.relative_to(app)), "bytes": path.stat().st_size,
                                 "sha256": digest.hexdigest()})
            except OSError as exc:
                manifest.append({"path": str(path.relative_to(app)), "error": str(exc)})
    write_json(capture / "final-file-manifest.json", manifest)
    # This is a fresh, dedicated repository. Intent-to-add makes new source files visible in the diff.
    status = subprocess.run(["git", "-C", str(app), "status", "--short", "--untracked-files=all"], capture_output=True)
    (capture / "git-status.txt").write_bytes(status.stdout + status.stderr)
    add = subprocess.run(["git", "-C", str(app), "add", "--intent-to-add", "--", "."], capture_output=True)
    (capture / "snapshot-errors.log").write_bytes(add.stderr)
    with (capture / "final-changes.patch").open("wb") as dest:
        diff = subprocess.run(["git", "-C", str(app), "diff", "--no-ext-diff", "--binary", "--", "."], stdout=dest, stderr=subprocess.PIPE)
    with (capture / "snapshot-errors.log").open("ab") as dest:
        dest.write(diff.stderr)
    return {"manifest_files": len(manifest), "git_status_exit": status.returncode,
            "git_intent_to_add_exit": add.returncode, "git_diff_exit": diff.returncode}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, default=HERE / "runs", help="Parent for new, uniquely named runs")
    parser.add_argument("--dry-run", action="store_true", help="Show the launch settings without creating files or calling a model")
    args = parser.parse_args()
    prompt_path = HERE / "build_prompt.txt"
    if not prompt_path.is_file():
        parser.error("build_prompt.txt must be beside this recorder")
    prompt = prompt_path.read_text(encoding="utf-8")
    codex = shutil.which("codex")
    if not codex:
        parser.error("Codex CLI is not installed or not on PATH")
    for dependency in ["git", "node", "npm"]:
        if not shutil.which(dependency):
            parser.error(f"{dependency} must be installed and on PATH before this run")
    try:
        preflight = load_model_preflight()
    except ValueError as exc:
        parser.error(str(exc))
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    root = args.runs_dir.expanduser().resolve() / run_id
    app, capture = root / "app", root / "capture"
    cmd = command_for(codex, app, capture)
    if args.dry_run:
        print("DRY RUN: no files created and no model request made.")
        print(f"Model: {MODEL}; reasoning effort: {EFFORT}; one agent; no fixed token target.")
        print(f"Found in local model catalog dated {preflight['catalog_fetched_at']}; live access not yet tested.")
        print("Workspace-write sandbox; project dependency downloads enabled; existing policy rules retained.")
        print("Command:", shlex.join(cmd))
        return 0
    root.mkdir(parents=True, exist_ok=False)
    app.mkdir(); capture.mkdir(mode=0o700)
    (app / ".gitignore").write_text(INITIAL_IGNORE, encoding="utf-8")
    subprocess.run(["git", "init", "--quiet", str(app)], check=True)
    (capture / "prompt.txt").write_text(prompt, encoding="utf-8")
    (capture / "initial-gitignore.txt").write_text(INITIAL_IGNORE, encoding="utf-8")
    shutil.copyfile(__file__, capture / "recorder.py")
    metadata = {"protocol": "pocketplan-one-agent-v2", "started_at_utc": utc_now(),
                "requested_model": MODEL, "requested_reasoning_effort": EFFORT,
                "model_preflight": preflight,
                "resolved_model_snapshot": None, "command": cmd, "platform": platform.platform(),
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "versions": [version_of([codex, "--version"]), version_of(["node", "--version"]),
                             version_of(["npm", "--version"]), version_of(["git", "--version"])],
                "initial_state": "Empty local Git repository plus recorder-supplied .gitignore",
                "user_config_loaded": False, "existing_policy_rules_retained": True,
                "single_agent": True, "codex_sessions_started_by_recorder": 1,
                "notes": ["One codex exec session makes multiple internal model calls.",
                          "The requested model alias is recorded; an immutable backend snapshot is not assumed.",
                          "System/project instructions, provider behavior and tool-output limits can affect reproduction.",
                          "Trace capture is external. Saving full build/test logs adds a small amount of work."]}
    write_json(capture / "run-metadata.json", metadata)
    env = os.environ.copy()
    env["NPM_CONFIG_CACHE"] = str(app / ".npm-cache")
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(app / ".cache" / "ms-playwright")
    events, invalid_lines, interrupted, proc = [], 0, False, None
    reported_errors = []
    started = time.monotonic()
    print(f"Starting {MODEL} ({EFFORT}). This makes real model requests using your existing Codex login.")
    print(f"App: {app}\nResearch record: {capture}", flush=True)
    try:
        with (capture / "events.jsonl").open("w", encoding="utf-8", buffering=1) as raw, \
             (capture / "timed-events.jsonl").open("w", encoding="utf-8", buffering=1) as timed, \
             (capture / "transcript.txt").open("w", encoding="utf-8", buffering=1) as transcript, \
             (capture / "codex.stderr.log").open("wb") as stderr:
            transcript.write("POCKETPLAN: OBSERVABLE CODEX EXECUTION TRACE\n\n")
            transcript.write("Contains emitted events, including available reasoning summaries. Private internal reasoning is not exposed.\n")
            transcript.write("Tool results may already be truncated by Codex; full build/test logs are requested separately.\n\n")
            transcript.write("EXACT USER PROMPT\n" + prompt + "\nEND USER PROMPT\n")
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                                    text=True, encoding="utf-8", errors="replace", env=env, start_new_session=True)
            try:
                proc.stdin.write(prompt)
                proc.stdin.close()
                for index, line in enumerate(proc.stdout, 1):
                    observed_at = utc_now()
                    raw.write(line)
                    try:
                        event = json.loads(line)
                        if not isinstance(event, dict):
                            raise ValueError("Event is not an object")
                    except (json.JSONDecodeError, ValueError):
                        invalid_lines += 1
                        timed.write(json.dumps({"received_at_utc": observed_at, "unparsed_line": line}) + "\n")
                        transcript.write(f"\nEVENT {index} | {observed_at} | UNPARSED\n{line}\n")
                        continue
                    events.append(event)
                    timed.write(json.dumps({"received_at_utc": observed_at, "event": event}, ensure_ascii=False) + "\n")
                    transcript.write(f"\nEVENT {index} | {observed_at}\n" + "\n".join(readable(event)) + "\n")
                    if event.get("type") == "thread.started":
                        metadata["thread_id"] = event.get("thread_id")
                        write_json(capture / "run-metadata.json", metadata)
                    item = event.get("item", {})
                    message = error_message(event)
                    if message:
                        if message not in reported_errors:
                            reported_errors.append(message)
                            print(f"Codex error: {message}", file=sys.stderr, flush=True)
                    elif event.get("type") == "item.completed" and isinstance(item, dict):
                        print(f"Recorded: {item.get('type', 'item')}", flush=True)
                proc.wait()
            except KeyboardInterrupt:
                interrupted = True
                transcript.write("\nRECORDER: interrupted by user; usage may be incomplete.\n")
                stop_process(proc)
            except BaseException:
                stop_process(proc)
                raise
    except Exception as exc:
        metadata["recorder_error"] = str(exc)
        print(f"Recorder error: {exc}", file=sys.stderr, flush=True)
    finally:
        metadata.update({"finished_at_utc": utc_now(), "elapsed_seconds": time.monotonic() - started,
                         "interrupted": interrupted, "codex_exit_code": proc.returncode if proc else None,
                         "reported_errors": reported_errors})
        usage = summarize_usage(events, invalid_lines)
        if interrupted or metadata["codex_exit_code"] != 0 or "recorder_error" in metadata:
            usage["status"] = "incomplete_or_unavailable"
        write_json(capture / "token-usage.json", usage)
        totals = usage["reported_totals"]
        lines = ["POCKETPLAN TOKEN USAGE", "Status: " + usage["status"], ""]
        lines += [key + ": " + (str(value) if value is not None else "NOT REPORTED") for key, value in totals.items()]
        lines += ["", *usage["notes"]]
        (capture / "token-usage.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        try:
            metadata["snapshot"] = snapshot(app, capture)
        except Exception as exc:
            metadata["snapshot_error"] = str(exc)
        write_json(capture / "run-metadata.json", metadata)
    print(f"\nSaved record: {capture}")
    print("Token status:", usage["status"])
    acceptance = app / "artifacts" / "acceptance-report.txt"
    if acceptance.is_file():
        print(f"App acceptance report: {acceptance}")
    else:
        print("No app acceptance report was produced; the app is not verified.")
    if metadata.get("codex_exit_code") != 0:
        print(f"Codex exited with status {metadata.get('codex_exit_code')}. "
              f"Diagnostics: {capture / 'codex.stderr.log'}")
    if metadata.get("codex_exit_code") != 0 or interrupted or "recorder_error" in metadata:
        return 1
    return 0 if usage["status"] == "reported_totals_available" else 2


if __name__ == "__main__":
    sys.exit(main())
