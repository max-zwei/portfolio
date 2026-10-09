#!/usr/bin/env python3
"""Offline, read-only device inventory. Never creates a Qt window or opens GPIO."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import grp
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(argv: list[str]) -> dict:
    executable = shutil.which(argv[0])
    if executable is None:
        return {"status": "unavailable", "command": argv}
    try:
        result = subprocess.run([executable, *argv[1:]], capture_output=True,
                                text=True, timeout=15, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "error", "command": argv, "error": type(exc).__name__}
    return {"status": "ok" if result.returncode == 0 else "error",
            "command": argv, "returncode": result.returncode,
            "stdout": result.stdout[:32768].strip(),
            "stderr": result.stderr[:4096].strip()}


def text_file(path: Path) -> dict:
    try:
        return {"status": "ok", "value": path.read_text().replace("\x00", "").strip()}
    except OSError as exc:
        return {"status": "unavailable", "error": type(exc).__name__}


def version_tuple(value: str) -> tuple[int, ...]:
    match = re.match(r"^(\d+)\.(\d+)", value)
    return tuple(map(int, match.groups())) if match else ()


def module_info(name: str, distribution: str) -> dict:
    # Top-level spec discovery only: in particular do not import GPIO libraries.
    try:
        available = importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        available = False
    try:
        version = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        version = None
    return {"available": available, "distribution_version": version}


def qt_inventory() -> dict:
    # Isolate binary imports so a broken Qt installation cannot abort the report.
    probe = '''import json
import PySide6
from PySide6 import QtCore, QtGui, QtQml, QtQuick, QtSvg
from pathlib import Path
plugins = Path(QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.PluginsPath))
qml = Path(QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.QmlImportsPath))
print(json.dumps({"qt_version": QtCore.qVersion(), "pyside_version": PySide6.__version__,
    "plugin_root": str(plugins), "qml_root": str(qml),
    "platforms": sorted(p.name for p in (plugins / "platforms").glob("*")),
    "egldeviceintegrations": sorted(p.name for p in (plugins / "egldeviceintegrations").glob("*")),
    "imageformats": sorted(p.name for p in (plugins / "imageformats").glob("*")),
    "qml_modules": {name: (qml / name / "qmldir").is_file() for name in
        ("QtQml", "QtQml/Models", "QtQml/WorkerScript", "QtQuick", "QtQuick/Window",
         "QtQuick/Layouts", "QtQuick/Controls", "QtQuick/Templates")}}))
'''
    result = command([sys.executable, "-c", probe])
    # Do not include the source code as a command in the public report.
    result.pop("command", None)
    if result["status"] == "ok":
        try:
            result["inventory"] = json.loads(result.pop("stdout"))
        except (ValueError, KeyError):
            result["status"] = "error"
            result["error"] = "Qt inventory did not return JSON"
    return result


def package_inventory(backend: str | None) -> dict:
    names = [line.split("#", 1)[0].strip() for line in
             (ROOT / "deploy/packages.txt").read_text().splitlines()]
    names = [name for name in names if name]
    if backend == "wayland":
        names += ["qt6-wayland", "weston"]
    result = command(["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\t${db:Status-Status}\n", *names])
    rows = {}
    for line in result.get("stdout", "").splitlines():
        fields = line.split("\t")
        if len(fields) == 3:
            rows[fields[0].split(":", 1)[0]] = {"version": fields[1], "status": fields[2]}
    result.pop("stdout", None)
    result["packages"] = rows
    result["missing"] = [name for name in names if rows.get(name, {}).get("status") != "installed"]
    return result


def device_nodes() -> list[dict]:
    nodes = []
    for pattern in ("dri/card*", "dri/renderD*", "input/event*", "gpiochip*", "tty0"):
        for path in sorted(Path("/dev").glob(pattern)):
            try:
                info = path.stat()
                nodes.append({"path": str(path), "mode": stat.filemode(info.st_mode),
                              "uid": info.st_uid, "gid": info.st_gid,
                              "readable": os.access(path, os.R_OK),
                              "writable": os.access(path, os.W_OK)})
            except OSError:
                nodes.append({"path": str(path), "status": "unavailable"})
    return nodes


def sensor_config(path: Path) -> dict:
    sys.path.insert(0, str(ROOT))
    from app.config import ConfigurationError, load_device
    try:
        settings = load_device(path).sensors
    except (ConfigurationError, OSError) as exc:
        # Config errors can contain arbitrary invalid input: report type, not content.
        return {"status": "invalid_or_missing", "error": type(exc).__name__}
    ready = (settings.hardware_verified and settings.pin_factory == "lgpio"
             and all(pin is not None for pin in settings.pins)
             and all(pin is not None for pin in settings.physical_pins))
    return {"status": "ok", "bcm_bottom_to_top": settings.pins,
            "header_bottom_to_top": settings.physical_pins,
            "wet_values": settings.wet_values, "pin_factory": settings.pin_factory,
            "hardware_verified_operator_assertion": settings.hardware_verified,
            "live_configuration_complete": ready,
            "electrical_safety_verified_by_preflight": False,
            "note": "Never connect GPIO before passive-contact verification; this report never opens GPIO."}


def process_memory(pid: int | None) -> dict:
    if pid is None:
        return {"status": "not_requested"}
    source = text_file(Path(f"/proc/{pid}/status"))
    if source["status"] != "ok":
        return source
    allowed = {"VmPeak", "VmSize", "VmHWM", "VmRSS", "RssAnon", "RssFile", "RssShmem", "VmSwap", "Threads"}
    return {"status": "ok", "pid": pid,
            "fields": {key: value.strip() for line in source["value"].splitlines()
                       if ":" in line for key, value in [line.split(":", 1)] if key in allowed}}


def collect(args: argparse.Namespace) -> dict:
    model = text_file(Path("/proc/device-tree/model"))
    architecture = command(["dpkg", "--print-architecture"])
    os_release = {}
    release = text_file(Path("/etc/os-release"))
    for line in release.get("value", "").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if key in {"ID", "ID_LIKE", "VERSION_ID", "VERSION_CODENAME", "PRETTY_NAME"}:
                os_release[key] = value.strip('"')
    pi_model = model.get("value", "").startswith("Raspberry Pi 3 Model A Plus")
    armhf = architecture.get("stdout") == "armhf" and struct.calcsize("P") == 4
    trixie = os_release.get("VERSION_CODENAME") == "trixie"
    target_eligible = platform.system() == "Linux" and pi_model and armhf and trixie
    qt = qt_inventory()
    inventory = qt.get("inventory", {})
    modules = {name: module_info(name, dist) for name, dist in
               (("PySide6", "PySide6"), ("segno", "segno"), ("gpiozero", "gpiozero"), ("lgpio", "lgpio"))}
    packages = package_inventory(args.display_backend)
    platforms = inventory.get("platforms", [])
    integrations = inventory.get("egldeviceintegrations", [])
    backend_available = False
    if args.display_backend == "eglfs":
        backend_available = "libqeglfs.so" in platforms and "libqeglfs-kms-integration.so" in integrations
    elif args.display_backend == "wayland":
        backend_available = "libqwayland-egl.so" in platforms and shutil.which("weston") is not None
    gpio_version = modules["gpiozero"]["distribution_version"] or ""
    segno_version = modules["segno"]["distribution_version"] or ""
    software_eligible = (not packages["missing"] and all(item["available"] for item in modules.values())
                         and (6, 8) <= version_tuple(inventory.get("qt_version", "")) < (7, 0)
                         and (6, 8) <= version_tuple(inventory.get("pyside_version", "")) < (7, 0)
                         and (2, 0) <= version_tuple(gpio_version) < (3, 0)
                         and (1, 6) <= version_tuple(segno_version) < (2, 0)
                         and all(inventory.get("qml_modules", {}).values())
                         and "libqsvg.so" in inventory.get("imageformats", []) and backend_available)
    config = sensor_config(args.device)
    connectors = []
    for path in sorted(Path("/sys/class/drm").glob("card*-*")):
        if (path / "status").exists():
            connectors.append({"name": path.name, "status": text_file(path / "status"),
                               "advertised_modes": text_file(path / "modes"),
                               "enabled": text_file(path / "enabled")})
    diagnostics = {
        "memory": command(["free", "-k"]),
        "swap": command(["swapon", "--show", "--bytes"]),
        "vmstat_snapshot": command(["vmstat", "-s"]),
        "throttled": command(["vcgencmd", "get_throttled"]),
        "temperature": command(["vcgencmd", "measure_temp"]),
        "thermal_zone0": text_file(Path("/sys/class/thermal/thermal_zone0/temp")),
        "rfkill": command(["rfkill", "--json"]),
        "bluetooth_service": command(["systemctl", "is-active", "bluetooth.service"]),
    }
    session = os.environ.get("XDG_SESSION_ID")
    diagnostics["session"] = (command(["loginctl", "show-session", session, "-p", "Active", "-p", "Type", "-p", "VTNr", "-p", "Seat"])
                              if session else {"status": "unavailable", "reason": "No XDG_SESSION_ID"})
    groups = []
    for gid in os.getgroups():
        try:
            groups.append(grp.getgrgid(gid).gr_name)
        except KeyError:
            groups.append(str(gid))
    blockers = []
    if not target_eligible:
        blockers.append("Requires Pi 3 Model A+, Linux Trixie armhf and a 32-bit Python interpreter.")
    if not software_eligible:
        blockers.append("Required packages, version ranges, QML/SVG plugins or explicitly selected backend are unavailable.")
    if not config.get("live_configuration_complete", False):
        blockers.append("Live GPIO configuration is incomplete/unverified; keep sensors disconnected.")
    blockers.append("Physical HDMI, GPU acceleration, keyboard reconnect, GPIO calibration, memory and power acceptance require operator evidence; inventory cannot certify them.")
    return {
        "schema_version": 1, "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Passive offline inventory; no window, modeset, GPIO open, network, keystroke or transcript capture.",
        "host": {"system": platform.system(), "kernel": platform.release(), "machine": platform.machine(),
                 "python": platform.python_version(), "python_bits": struct.calcsize("P") * 8,
                 "model": model, "dpkg_architecture": architecture, "os_release": os_release},
        "eligibility": {"pi_model_matches": pi_model, "armhf_userspace": armhf, "trixie": trixie,
                        "target_eligible": target_eligible, "software_baseline_eligible": software_eligible,
                        "selected_backend_plugins_present": backend_available,
                        "physical_acceptance_verified": False},
        "display": {"selected_backend": args.display_backend, "target_pixels": [1280, 720],
                    "environment": {key: os.environ.get(key) for key in
                        ("QT_QPA_PLATFORM", "QT_QPA_EGLFS_INTEGRATION", "QT_QPA_EGLFS_KMS_CONFIG",
                         "QSG_RHI_BACKEND", "QT_QUICK_BACKEND", "DISPLAY", "WAYLAND_DISPLAY",
                         "XDG_RUNTIME_DIR", "XDG_SESSION_TYPE")}, "connectors": connectors,
                    "note": "Advertised modes and plugin filenames do not prove the current rendered mode or acceleration."},
        "identity": {"euid": os.geteuid(), "groups": sorted(groups)},
        "modules": modules, "packages": packages, "qt": qt, "device_nodes": device_nodes(),
        "sensors": config, "diagnostics": diagnostics, "process_memory": process_memory(args.pid),
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--display-backend", choices=("eglfs", "wayland"),
                        help="explicit intended backend; no selection means not software-eligible")
    parser.add_argument("--device", type=Path, default=ROOT / "config/device.json")
    parser.add_argument("--output", default="-", help="JSON stdout (-) or NEW private output file; never overwrites")
    parser.add_argument("--pid", type=int, help="optional application PID: memory counters only, never command line or session text")
    parser.add_argument("--require-pi", action="store_true", help="exit 2 unless fixed target model/OS/architecture match")
    parser.add_argument("--require-software", action="store_true", help="exit 2 unless selected packaged software inventory is eligible")
    args = parser.parse_args()
    if args.pid is not None and args.pid <= 0:
        parser.error("--pid must be positive")
    report = collect(args)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output == "-":
        sys.stdout.write(payload)
    else:
        try:
            descriptor = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "w") as destination:
                destination.write(payload)
        except OSError as exc:
            parser.exit(1, f"Cannot create evidence file: {exc}\n")
    eligibility = report["eligibility"]
    if ((args.require_pi and not eligibility["target_eligible"])
            or (args.require_software and not eligibility["software_baseline_eligible"])):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
