"""Native, offline Qt Quick runtime with explicit mock or live sensing.

--mock-file accepts an externally replaced JSON object containing only
{"raw_bits": [1, 1, 0, 0, 0]} or {"read_failure": true}. Bits are physical,
bottom to top; missing/malformed input is unknown, never an assumed full tank.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import signal
import sys
from typing import Sequence

from .config import ConfigurationError, DeviceSettings, ScriptConfig, load_device, load_script
from .contracts import Mode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="thirsty — local water-dependent Qt performance")
    parser.add_argument("--mode", choices=[mode.value for mode in Mode], required=True,
                        help="explicit sensor mode; live never falls back to mock")
    parser.add_argument("--device", type=Path, default=Path("config/device.json"), help="device settings JSON path")
    parser.add_argument("--script", type=Path, default=Path("config/script.json"), help="script JSON with operator-provided repository URL")
    parser.add_argument("--fullscreen", action="store_true", help="override device settings to use fullscreen")
    parser.add_argument("--mock-file", type=Path, help="mock mode only: externally replaceable raw-input JSON")
    return parser


class MockFileInput:
    """Read local raw-input control without caching stale success on file errors."""

    def __init__(self, path: Path, adapter) -> None:
        self.path = path
        self.adapter = adapter
        self._version: tuple[int, int, int] | None = None
        self._unreadable = False

    def poll(self) -> None:
        try:
            stat = self.path.stat()
            version = (stat.st_ino, stat.st_mtime_ns, stat.st_size)
            if version == self._version:
                return
            value = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or set(value) not in ({"raw_bits"}, {"read_failure"}):
                raise ValueError("expected only raw_bits or read_failure")
            if "read_failure" in value:
                if value["read_failure"] is not True:
                    raise ValueError("read_failure must be true")
                self.adapter.setReadFailure(True)
            else:
                bits = value["raw_bits"]
                if not isinstance(bits, list) or len(bits) != 5 or any(type(bit) is not int or bit not in (0, 1) for bit in bits):
                    raise ValueError("raw_bits must be five physical 0/1 integers")
                self.adapter.setRawBits(bits)
                self.adapter.setReadFailure(False)
            self._version = version
            self._unreadable = False
        except (OSError, UnicodeError, ValueError):
            self._version = None
            self.adapter.setReadFailure(False)
            self.adapter.setRawBits(None)
            if not self._unreadable:
                # Never print file contents: external input may contain private text.
                print("Operator mock input error: file missing, unreadable or invalid; sensing is unknown.", file=sys.stderr)
                self._unreadable = True


def _run_application(args: argparse.Namespace, settings: DeviceSettings, script: ScriptConfig) -> int:
    # Keep configuration diagnostics usable independently of Qt installation.
    from PySide6.QtCore import QTimer, QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine

    from .controller import ExperienceController
    from .handoff import repository_qr_source
    from .sensors import GPIOSensorAdapter, MockSensorAdapter

    application = QGuiApplication([sys.argv[0]])
    application.setApplicationName("thirsty")
    controller = ExperienceController(settings, script)
    controller.setQrSource(repository_qr_source(script.repository_url))
    sensor = (MockSensorAdapter(settings.sensors) if args.mode == "mock"
              else GPIOSensorAdapter(settings.sensors))
    sensor.readingChanged.connect(controller.receiveReading)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", controller)
    engine.setInitialProperties({
        "appWidth": settings.display.width,
        "appHeight": settings.display.height,
        "appFullscreen": args.fullscreen or settings.display.fullscreen,
    })
    control_timer = QTimer()
    control_timer.setInterval(settings.sensors.poll_interval_ms)
    if args.mock_file is not None:
        mock_input = MockFileInput(args.mock_file, sensor)
        mock_input.poll()
        control_timer.timeout.connect(mock_input.poll)
    # A Python callback lets CPython deliver SIGINT/SIGTERM while Qt is idle.
    signal_timer = QTimer()
    signal_timer.setInterval(100)
    signal_timer.timeout.connect(lambda: None)
    previous_handlers = {}
    stopped = False
    cleanup_error = None
    shutdown_requested = False

    def stop() -> None:
        nonlocal stopped, cleanup_error
        if stopped:
            return
        stopped = True
        control_timer.stop()
        signal_timer.stop()
        try:
            sensor.stop()
        except Exception as exc:
            cleanup_error = exc
            print(f"Operator shutdown error: {exc}", file=sys.stderr)

    def request_shutdown(_signum, _frame) -> None:
        nonlocal shutdown_requested
        shutdown_requested = True
        application.quit()

    application.aboutToQuit.connect(stop)
    try:
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.signal(signum, request_shutdown)
        signal_timer.start()
        try:
            sensor.start()
        except Exception as exc:
            raise RuntimeError(f"Cannot initialize {args.mode} sensors: {exc}") from exc
        if args.mock_file is not None:
            control_timer.start()
        engine.load(QUrl.fromLocalFile(str(Path(__file__).parent / "ui" / "Main.qml")))
        if not engine.rootObjects():
            raise RuntimeError("the native QML application window could not be loaded")
        result = 0 if shutdown_requested else application.exec()
    finally:
        stop()
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)
    return 1 if cleanup_error is not None else result


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.mock_file is not None and args.mode != "mock":
        parser.error("--mock-file is permitted only with explicit --mode mock")
    try:
        settings = load_device(args.device)
        settings.validate_for_mode(args.mode)
        script = load_script(args.script)
        return _run_application(args, settings, script)
    except ConfigurationError as exc:
        print(f"Operator configuration error: {exc}", file=sys.stderr)
        return 2
    except ImportError as exc:
        print(f"Operator dependency error: {exc}. Install the project dependencies for this Python interpreter.", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"Operator application error: {exc}", file=sys.stderr)
        return 1
