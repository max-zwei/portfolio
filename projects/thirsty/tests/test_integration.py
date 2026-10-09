"""Offline integration regressions; synthetic ideas and labeled fixture URL only."""

import base64
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QImage
import segno

from app.config import DeviceSettings, load_script
from app.controller import ExperienceController
from app.handoff import repository_qr_source
from app.main import MockFileInput, build_parser, main
from app.sensors import MockSensorAdapter


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_URL = "https://example.org/integration-test-fixture"


@pytest.fixture
def qt_application():
    application = QCoreApplication.instance() or QCoreApplication([])
    return application


def test_cli_requires_explicit_mode(capsys):
    parser = build_parser()
    with pytest.raises(SystemExit) as error:
        parser.parse_args([])
    assert error.value.code == 2
    assert "--mode" in capsys.readouterr().err


def test_unverified_live_pins_fail_before_qt(capsys):
    assert main(["--mode", "live", "--device", str(ROOT / "config/device.json"),
                 "--script", str(ROOT / "config/script.json")]) == 2
    assert "Operator configuration error" in capsys.readouterr().err


def test_qr_exact_pixels_and_four_module_quiet_zone():
    source = repository_qr_source(FIXTURE_URL)
    assert source.startswith("data:image/png;base64,")
    image = QImage.fromData(base64.b64decode(source.partition(",")[2]), "PNG")
    assert (image.width(), image.height()) == (208, 208)
    code = segno.make_qr(FIXTURE_URL, error="m")
    modules = code.symbol_size(scale=1, border=4)[0]
    scale = 208 // modules
    offset = (208 - modules * scale) // 2
    matrix = list(code.matrix_iter(scale=scale, border=4))
    # Compare every raster pixel, including integer modules and centered padding.
    for y in range(208):
        for x in range(208):
            inside = offset <= x < offset + len(matrix) and offset <= y < offset + len(matrix)
            dark = inside and matrix[y - offset][x - offset]
            assert image.pixelColor(x, y).name() == ("#000000" if dark else "#ffffff")


def test_external_input_drives_real_controller_and_resets(qt_application, tmp_path, capsys):
    now = [0.0]
    clock = lambda: now[0]
    settings = DeviceSettings()
    script = replace(load_script(ROOT / "config/script.json"), repository_url=FIXTURE_URL)
    controller = ExperienceController(settings, script, clock=clock, auto_timers=False)
    adapter = MockSensorAdapter(settings.sensors, clock=clock, auto_timers=False)
    adapter.readingChanged.connect(controller.receiveReading)
    path = tmp_path / "raw.json"
    control = MockFileInput(path, adapter)
    source = repository_qr_source(script.repository_url)
    controller.setQrSource(source)

    def raw(value):
        replacement = tmp_path / "replacement.json"
        replacement.write_text(json.dumps(value), encoding="utf-8")
        replacement.replace(path)
        control.poll()
        adapter.poll()

    def advance(milliseconds):
        for _ in range((milliseconds + 49) // 50):
            now[0] += 0.05
            adapter.poll()
            controller.tick()

    try:
        adapter.start()
        controller.start()
        controller.submit("Synthetic integration idea")
        assert controller.state == "paused_sensor"
        raw({"raw_bits": [1, 1, 1, 1, 1]})
        advance(settings.sensors.stable_for_ms + settings.interaction.refill_hold_ms + 100)
        assert controller.state == "running"
        raw({"raw_bits": [0, 0, 0, 0, 0]})
        advance(settings.sensors.stable_for_ms + 100)
        assert controller.state == "paused_water"
        raw({"raw_bits": [1, 1, 1, 1, 1]})
        advance(settings.sensors.stable_for_ms + settings.interaction.refill_hold_ms + 100)
        assert controller.state == "running"
        raw({"read_failure": True})
        assert controller.state == "paused_sensor"
        # Malformed external input clears success, does not leak its contents.
        raw({"private": "Never print synthetic visitor content"})
        assert controller.sensorStatus == "unknown"
        assert "Never print" not in capsys.readouterr().err
        raw({"raw_bits": [1, 1, 1, 1, 1]})
        advance(settings.sensors.stable_for_ms + settings.interaction.refill_hold_ms + 100)
        advance(sum(step.delay_ms for step in script.progress) + 100)
        assert controller.state == "finished"
        model = controller.transcript
        id_role = next(role for role, name in model.roleNames().items() if name == b"id")
        identifiers = [
            model.data(model.index(index, 0), id_role)
            for index in range(model.rowCount())
        ]
        assert [
            identifier for identifier in identifiers
            if identifier.startswith(("progress:", "summary:"))
        ] == [
            *(f"progress:{step.id}" for step in script.progress),
            *(f"summary:{row.id}" for row in script.final_summary),
        ]
        controller.reset()
        assert controller.state == "start"
        assert controller.idea == ""
        assert controller.transcript.rowCount() == 0
        assert controller.qrSource == source
        assert controller.sensorStatus == "unknown"
    finally:
        adapter.stop()


def test_native_qml_runtime_exits_cleanly_on_sigterm(tmp_path):
    """Use real Qt in a child, isolated from controller tests' QCoreApplication."""
    raw = tmp_path / "raw.json"
    raw.write_text('{"raw_bits": [1, 1, 1, 1, 1]}', encoding="utf-8")
    program = '''
import os
import signal
from app.main import main
# Keep runtime unchanged; OS signal comes from a separate Python thread.
import threading
shutdown = threading.Timer(2, lambda: os.kill(os.getpid(), signal.SIGTERM))
shutdown.start()
try:
    raise SystemExit(main(["--mode", "mock", "--device", "config/device.json",
                           "--script", "config/script.json", "--mock-file", os.environ["RAW_FILE"]]))
finally:
    shutdown.cancel()
'''
    environment = dict(os.environ, QT_QPA_PLATFORM="offscreen", QSG_RHI_BACKEND="software", RAW_FILE=str(raw))
    result = subprocess.run([sys.executable, "-c", program], cwd=ROOT, env=environment,
                            capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert "failed to load component" not in result.stderr.lower()
    assert "ReferenceError" not in result.stderr
    assert "TypeError" not in result.stderr
