POCKETPLAN: ONE RECORDED CODEX APP BUILD

Purpose
Build one modest mobile task-planning app and measure the recorded token usage.
This is a defined case study, not evidence of an industry-average app budget.
The app uses Expo, React Native and TypeScript, with five screens and local data.
No backend account or real personal data is required. Exact requirements are in
build_prompt.txt.

Fixed requested settings
Model: GPT-6.1-Sol (gpt-6.1-sol)
Reasoning effort: medium
One agent; delegation and memory features disabled; fresh app directory.
No fixed token target and no artificial extra iterations.
The launcher checks the fixed model and effort against your local Codex model
catalog before starting. This cached check is not a live access guarantee. If
the catalog is missing or outdated, refresh it through Codex's model picker.
The actual request may still fail; preserve the record and do not silently
replace the model. The alias may change on the server:
this protocol records the requested alias and date, not an unreported snapshot.

Start the experiment
Use a computer with Python 3, Git, Node.js, npm and a signed-in Codex CLI.
The launcher uses the existing Codex login. Running it makes real model requests
and uses your account's allowance or API billing, according to that login.

From this folder:
  python3 run_recorded_build.py --dry-run
  python3 run_recorded_build.py

The dry run does not contact a model or create a run directory. The second
command creates runs/<unique-run-id>/app and runs/<unique-run-id>/capture.
Each invocation is a NEW experiment. Do not rerun to continue the same build.
There is no automatic retry, no model fallback and no resume loop.

The actual command uses codex exec --json and an external recorder, rather than
asking the model to estimate its own usage or reconstruct a transcript later.
The personal Codex config file is ignored for a more consistent environment;
existing policy rules are retained. It uses the workspace-write sandbox and
enables network access for project dependency downloads. It does not use
danger-full-access or bypass sandbox/approval enforcement. Non-interactive
approval policy is never: requests outside the allowed sandbox fail and must be
reported. If a required permission or model is unavailable, the recorded run may
end incomplete. Do not quietly change those constraints during a comparison.

What is recorded
capture/prompt.txt               Exact initial user prompt.
capture/run-metadata.json        Model setting, filtered catalog check,
                                CLI/runtime versions, command, timestamps,
                                exit status, errors and prompt hash.
capture/events.jsonl             Raw stdout events as emitted by Codex.
capture/timed-events.jsonl       Same events plus receipt timestamps.
capture/transcript.txt           Readable chronological event transcript.
capture/codex.stderr.log         CLI progress, diagnostics and failures.
capture/final-message.txt        Final agent answer, kept separately.
capture/token-usage.json         Raw completion usage and aggregated counters.
capture/token-usage.txt          Readable token totals and limitations.
capture/final-changes.patch      Final source changes in the fresh repository.
capture/final-file-manifest.json File hashes, including app verification logs.
app/                            Complete app source and lockfile.
app/artifacts/command-logs/      Full install/build/test logs, saved by the agent.
app/artifacts/acceptance-report.txt
                                Actual verification outcomes and limitations.

What 'full script' means
The transcript captures all events emitted to this CLI event stream, including
agent messages, tool/command activity, reported outputs, file-change events,
errors and any exposed reasoning summaries. It is not a shell script to replay
blindly: some operations are tool calls or file patches rather than shell commands.
It does not reveal private internal chain-of-thought, hidden provider operations,
or a verbatim copy of every request sent to the model. Some emitted tool results
may already be truncated. Full build/test logs and the final source snapshot
supplement the event stream; completeness should be reviewed after the run.

Token accounting
Only usage attached to turn.completed is summed, not every lifecycle event.
Cached input is a subset of input and is not added again. Reasoning output is
recorded separately when reported; it is not added again to output. Missing
fields remain null/NOT REPORTED. On failure or interruption, usage may be missing
or partial; such a run is marked incomplete. Do not substitute guessed values.
The session can contain many model calls inside one completed agent turn.
Reported usage is not an independent audit of provider-side retries or billing.

Measurement boundary
Count the complete build, including failed attempts, debugging and verification.
Do not select only the most efficient successful segment. Note any environment
repair or human intervention separately. CLI success does not by itself prove
that the app passed its acceptance criteria. Web testing is not native testing.
No new water figure is calculated by this package. Token counts alone cannot
establish Codex electricity consumption, and the earlier Llama 2 benchmark water
factor must not be relabeled as measured Codex water consumption.

Portfolio integration
This directory is a standalone recorded experiment, not part of the Astro site.
The portfolio's TypeScript and formatting checks exclude it so the recorded
source and capture files stay unchanged. Run the app's own verification commands
from app/ as documented in app/README.md. Generated dependencies, caches, build
output and app artifacts remain local under app/.gitignore.

Preparation validation
This package was checked against Codex CLI 0.159.3 and tested with synthetic event
streams. Those checks make no model calls and are not the app-building experiment.

Protocol amendment: October 9, 2026 (v2)
The original v1 launcher requested gpt-5.3-codex. Run
20261009T061411Z-a7fa3e54 failed because the service returned HTTP 400:
"The 'gpt-5.3-codex' model is not supported when using Codex with a ChatGPT account."
No app build was completed and no token totals were reported. Missing usage does
not mean zero usage. The original run, including its original recorder and model
setting, is retained unchanged.

The fixed model is now gpt-6.1-sol, at the same medium reasoning effort. The local
Codex catalog fetched on October 9, 2026 at 06:15:03 UTC listed this model and
supported medium effort. This is a documented protocol change, not a fallback
within a run. The app prompt and acceptance requirements are unchanged. A new
launch starts a new run. The launcher now checks cached model metadata, displays
actual service errors, and reports when no acceptance report was produced.
Only the selected model's metadata is saved; account identity data is excluded.

Documentation consulted (accessed October 9, 2026)
OpenAI. (n.d.). Codex models. Retrieved October 9, 2026, from
https://developers.openai.com/codex/models
This page confirms gpt-5.3-codex deprecation for ChatGPT sign-in. The replacement
model choice is supported by the local Codex catalog, not this public page.

OpenAI. (n.d.). Non-interactive mode.
https://developers.openai.com/codex/noninteractive
OpenAI. (n.d.). Codex CLI reference.
https://developers.openai.com/codex/cli/reference
OpenAI. (n.d.). Configuration reference.
https://developers.openai.com/codex/config-reference
OpenAI. (n.d.). Reasoning models.
https://developers.openai.com/api/docs/guides/reasoning
