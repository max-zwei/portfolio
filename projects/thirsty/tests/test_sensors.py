"""Consumer-visible adapter tests; fake GPIO lifecycle is not hardware evidence."""

from dataclasses import replace
from itertools import product
from types import SimpleNamespace

import pytest
from PySide6.QtCore import QObject, QThread, QTimer, Slot
from PySide6.QtGui import QGuiApplication

from app.config import ConfigurationError, SensorSettings
from app.contracts import SensorReading
from app import sensors
from app.sensors import GPIOSensorAdapter, MockSensorAdapter


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


@pytest.fixture(scope="module", autouse=True)
def qt_application():
    # Use QGuiApplication so later integrated QML tests can share this instance.
    app = QGuiApplication.instance() or QGuiApplication(["sensor-tests", "-platform", "offscreen"])
    yield app


@pytest.fixture
def mock():
    clock = Clock()
    adapter = MockSensorAdapter(SensorSettings(), clock=clock, auto_timers=False)
    readings = []
    adapter.readingChanged.connect(readings.append)
    yield adapter, clock, readings
    adapter.stop()


def poll_at(adapter, clock, readings, when):
    clock.now = when
    adapter.poll()
    return readings[-1]


def accept(adapter, clock, readings, bits=(1, 1, 1, 0, 0)):
    adapter.setRawBits(bits)
    adapter.start()
    return poll_at(adapter, clock, readings, 0.2)


@pytest.mark.parametrize("wet", [(1, 1, 1, 1, 1), (0, 0, 0, 0, 0), (0, 1, 0, 1, 0)])
@pytest.mark.parametrize("normalized", list(product((0, 1), repeat=5)))
def test_all_32_patterns_and_polarities(normalized, wet):
    clock = Clock()
    adapter = MockSensorAdapter(SensorSettings(wet_values=wet), clock=clock, auto_timers=False)
    readings = []
    adapter.readingChanged.connect(readings.append)
    raw = tuple(polarity if bit else 1 - polarity for bit, polarity in zip(normalized, wet))
    adapter.setRawBits(raw)
    try:
        adapter.start()
        assert readings[-1] == SensorReading(raw, None, "unknown", 0.0, False)
        assert poll_at(adapter, clock, readings, 0.199).status == "unknown"
        reading = poll_at(adapter, clock, readings, 0.2)
        level = sum(normalized)
        valid = normalized == (1,) * level + (0,) * (5 - level)
        assert reading == SensorReading(raw, level if valid else None, "ok" if valid else "fault", 0.2, True)
    finally:
        adapter.stop()


def test_startup_is_unknown_and_start_is_idempotent(mock):
    adapter, clock, readings = mock
    adapter.start()
    assert readings == [SensorReading(None, None, "unknown", None, False)]
    adapter.start()
    assert len(readings) == 1
    assert poll_at(adapter, clock, readings, 10) == readings[0]


def test_each_steady_poll_refreshes_heartbeat_timestamp(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    for when in (0.25, 0.5, 1.0, 1.5, 2.0):
        count = len(readings)
        reading = poll_at(adapter, clock, readings, when)
        assert len(readings) == count + 1
        assert reading == SensorReading((1, 1, 1, 0, 0), 3, "ok", when, True)


def test_candidate_keeps_last_accepted_level_but_blocks_progress(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    adapter.setRawBits((0, 0, 0, 0, 0))
    reading = poll_at(adapter, clock, readings, 0.3)
    assert reading == SensorReading((0, 0, 0, 0, 0), 3, "ok", 0.3, False)
    assert not poll_at(adapter, clock, readings, 0.499).is_stable
    assert poll_at(adapter, clock, readings, 0.5) == SensorReading((0, 0, 0, 0, 0), 0, "ok", 0.5, True)


def test_bounce_restarts_full_window_even_returning_to_accepted_pattern(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    adapter.setRawBits((1, 0, 0, 0, 0))
    poll_at(adapter, clock, readings, 0.3)
    adapter.setRawBits((1, 1, 1, 0, 0))
    assert not poll_at(adapter, clock, readings, 0.4).is_stable
    adapter.setRawBits((1, 0, 0, 0, 0))
    assert not poll_at(adapter, clock, readings, 0.5).is_stable
    assert poll_at(adapter, clock, readings, 0.699).level == 3
    assert poll_at(adapter, clock, readings, 0.7) == SensorReading((1, 0, 0, 0, 0), 1, "ok", 0.7, True)


def test_invalid_pattern_faults_only_after_stability_and_recovers_after_new_window(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    adapter.setRawBits((0, 1, 0, 0, 0))
    assert poll_at(adapter, clock, readings, 0.3).level == 3
    assert poll_at(adapter, clock, readings, 0.5) == SensorReading((0, 1, 0, 0, 0), None, "fault", 0.5, True)
    adapter.setRawBits((1, 0, 0, 0, 0))
    assert poll_at(adapter, clock, readings, 0.6) == SensorReading((1, 0, 0, 0, 0), None, "fault", 0.6, False)
    assert poll_at(adapter, clock, readings, 0.8).level == 1


@pytest.mark.parametrize("stable_ms", [0, 375])
def test_configurable_stabilization(stable_ms):
    clock = Clock()
    adapter = MockSensorAdapter(SensorSettings(stable_for_ms=stable_ms), clock=clock, auto_timers=False)
    readings = []
    adapter.readingChanged.connect(readings.append)
    adapter.setRawBits((1, 1, 1, 1, 1))
    try:
        adapter.start()
        if stable_ms:
            assert not poll_at(adapter, clock, readings, (stable_ms - 1) / 1000).is_stable
        assert poll_at(adapter, clock, readings, stable_ms / 1000).level == 5
    finally:
        adapter.stop()


def test_read_failure_is_immediate_retains_raw_timestamp_and_eventually_stales(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    adapter.setReadFailure(True)
    for when in (0.201, 0.5, 1.199):
        assert poll_at(adapter, clock, readings, when) == SensorReading((1, 1, 1, 0, 0), None, "fault", 0.2, False)
    for when in (1.2, 1.5, 100):
        assert poll_at(adapter, clock, readings, when) == SensorReading((1, 1, 1, 0, 0), None, "unknown", 0.2, False)


def test_failed_startup_never_invents_successful_timestamp(mock):
    adapter, clock, readings = mock
    adapter.setReadFailure(True)
    adapter.start()
    assert readings[-1] == SensorReading(None, None, "fault", None, False)
    assert poll_at(adapter, clock, readings, 10) == readings[0]
    adapter.setReadFailure(False)
    assert poll_at(adapter, clock, readings, 11) == SensorReading(None, None, "unknown", None, False)


def test_failure_breaks_debounce_and_recovery_requires_stability(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    adapter.setReadFailure(True)
    poll_at(adapter, clock, readings, 0.21)
    adapter.setReadFailure(False)
    assert poll_at(adapter, clock, readings, 0.3) == SensorReading((1, 1, 1, 0, 0), None, "fault", 0.3, False)
    assert not poll_at(adapter, clock, readings, 0.499).is_stable
    assert poll_at(adapter, clock, readings, 0.5).level == 3


def test_unknown_mock_input_retains_last_success_and_requires_new_stability(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    adapter.setRawBits(None)
    assert poll_at(adapter, clock, readings, 0.3) == SensorReading((1, 1, 1, 0, 0), None, "unknown", 0.2, False)
    assert poll_at(adapter, clock, readings, 3).sampled_at == 0.2
    adapter.setRawBits([1, 1, 1, 0, 0])
    assert poll_at(adapter, clock, readings, 4) == SensorReading((1, 1, 1, 0, 0), None, "unknown", 4, False)
    assert poll_at(adapter, clock, readings, 4.2).level == 3


@pytest.mark.parametrize("gap,stable", [(0.999, True), (1.0, False), (1.001, False)])
def test_stale_polling_gap_cannot_count_as_continuous_stability(mock, gap, stable):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    reading = poll_at(adapter, clock, readings, 0.2 + gap)
    assert reading.is_stable is stable
    assert reading.status == ("ok" if stable else "unknown")
    assert reading.sampled_at == 0.2 + gap


def test_stale_timeout_is_configurable():
    clock = Clock()
    adapter = MockSensorAdapter(SensorSettings(stale_after_ms=500), clock=clock, auto_timers=False)
    readings = []
    adapter.readingChanged.connect(readings.append)
    try:
        accept(adapter, clock, readings)
        adapter.setReadFailure(True)
        assert poll_at(adapter, clock, readings, 0.699).status == "fault"
        assert poll_at(adapter, clock, readings, 0.7).status == "unknown"
        assert readings[-1].sampled_at == 0.2
    finally:
        adapter.stop()


@pytest.mark.parametrize("bits", [(1, 1), (0,) * 6, (True, 0, 0, 0, 0), (1.0, 0, 0, 0, 0), (2, 0, 0, 0, 0), "10000", 5])
def test_invalid_mock_bits_rejected_without_changing_input(mock, bits):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    with pytest.raises(ValueError, match="five bottom-to-top"):
        adapter.setRawBits(bits)
    assert poll_at(adapter, clock, readings, 0.25).level == 3


@pytest.mark.parametrize("failed", [0, 1, None, "false"])
def test_failure_toggle_requires_boolean(mock, failed):
    with pytest.raises(ValueError, match="boolean"):
        mock[0].setReadFailure(failed)


def test_mock_setter_copies_mutable_list_and_does_not_emit(mock):
    adapter, clock, readings = mock
    bits = [1, 1, 0, 0, 0]
    adapter.setRawBits(bits)
    bits[0] = 0
    adapter.setReadFailure(False)
    assert readings == []
    adapter.start()
    assert poll_at(adapter, clock, readings, 0.2).level == 2


def test_shutdown_is_idempotent_and_restart_reinitializes(mock):
    adapter, clock, readings = mock
    accept(adapter, clock, readings)
    clock.now = 0.3
    adapter.stop()
    assert readings[-1] == SensorReading((1, 1, 1, 0, 0), None, "unknown", 0.2, False)
    count = len(readings)
    adapter.stop()
    assert len(readings) == count
    assert poll_at(adapter, clock, readings, 0.5).sampled_at == 0.2
    adapter.start()
    assert readings[-1] == SensorReading((1, 1, 1, 0, 0), None, "unknown", 0.5, False)
    assert poll_at(adapter, clock, readings, 0.7).level == 3


def test_qt_timer_connection_and_delivery_on_owner_thread():
    clock = Clock()
    adapter = MockSensorAdapter(SensorSettings(poll_interval_ms=37), clock=clock)

    class Consumer(QObject):
        def __init__(self):
            super().__init__()
            self.received = []

        @Slot(object)
        def receive(self, reading):
            self.received.append((reading, QThread.currentThread()))

    consumer = Consumer()
    adapter.readingChanged.connect(consumer.receive)
    adapter.setRawBits((1, 0, 0, 0, 0))
    timer = adapter.findChild(QTimer)
    try:
        adapter.start()
        assert timer.isActive()
        assert timer.interval() == 37
        clock.now = 0.2
        # Deterministically exercise the real timeout connection, no wall time.
        timer.timeout.emit()
        assert consumer.received[-1][0].level == 1
        assert all(thread == adapter.thread() for _, thread in consumer.received)
    finally:
        adapter.stop()
    assert not timer.isActive()


def test_manual_mode_never_arms_timer(mock):
    mock[0].start()
    assert not mock[0].findChild(QTimer).isActive()


class FakeGPIO:
    """Lifecycle injection only: no claims about pins, wiring or Pi support."""

    def __init__(self):
        self.imports = []
        self.devices = []
        self.factories = []
        self.values = {27: 0, 2: 1, 17: 0, 4: 0, 3: 1}
        self.fail_open_at = None
        self.fail_read_pin = None
        self.fail_close_pin = None
        self.fail_factory = False
        self.fail_factory_close = False
        owner = self

        class Factory:
            def __init__(self):
                if owner.fail_factory:
                    raise OSError("backend unavailable")
                self.close_count = 0
                owner.factories.append(self)

            def close(self):
                self.close_count += 1
                if owner.fail_factory_close:
                    raise OSError("factory close failed")

        class Input:
            def __init__(self, pin, *, pull_up, pin_factory):
                if len(owner.devices) == owner.fail_open_at:
                    raise OSError("input open failed")
                self.pin = pin
                self.pull_up = pull_up
                self.factory = pin_factory
                self.close_count = 0
                owner.devices.append(self)

            @property
            def value(self):
                if self.pin == owner.fail_read_pin:
                    raise OSError("input read failed")
                return owner.values[self.pin]

            def close(self):
                self.close_count += 1
                if self.pin == owner.fail_close_pin:
                    raise OSError("input close failed")

        self.Input = Input
        self.Factory = Factory

    def import_module(self, name):
        self.imports.append(name)
        if name == "gpiozero":
            return SimpleNamespace(DigitalInputDevice=self.Input)
        for module, class_name in sensors._FACTORIES.values():
            if name == module:
                return SimpleNamespace(**{class_name: self.Factory})
        raise ImportError(name)


@pytest.fixture
def gpio(monkeypatch):
    fake = FakeGPIO()
    monkeypatch.setattr(sensors, "import_module", fake.import_module)
    monkeypatch.delenv("GPIOZERO_PIN_FACTORY", raising=False)
    return fake


def live_settings(**kwargs):
    return replace(SensorSettings(pins=(27, 2, 17, 4, 3), wet_values=(0, 1, 0, 1, 0), pin_factory="native"), **kwargs)


def test_mock_never_imports_gpio(monkeypatch):
    def forbidden(name):
        raise AssertionError(f"unexpected GPIO import: {name}")

    monkeypatch.setattr(sensors, "import_module", forbidden)
    adapter = MockSensorAdapter(SensorSettings(), auto_timers=False)
    adapter.start()
    adapter.stop()


def test_live_missing_pins_rejected_before_import(gpio):
    with pytest.raises(ConfigurationError, match="five configured, distinct"):
        GPIOSensorAdapter(SensorSettings(), auto_timers=False)
    assert gpio.imports == []


def test_duplicate_pin_configuration_rejected(gpio):
    with pytest.raises(ConfigurationError, match="distinct"):
        GPIOSensorAdapter(SensorSettings(pins=(2, 2, 3, 4, 5)), auto_timers=False)
    assert gpio.imports == []


def test_live_missing_package_is_explicit_no_fallback(monkeypatch):
    def missing(name):
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(sensors, "import_module", missing)
    with pytest.raises(RuntimeError, match="GPIO Zero"):
        GPIOSensorAdapter(live_settings(), auto_timers=False)


@pytest.mark.parametrize("factory", ["lgpio", "rpigpio", "pigpio", "native"])
def test_configured_backend_order_polarity_pull_down_and_cleanup(gpio, factory):
    clock = Clock()
    adapter = GPIOSensorAdapter(live_settings(pin_factory=factory), clock=clock, auto_timers=False)
    readings = []
    adapter.readingChanged.connect(readings.append)
    assert gpio.imports == ["gpiozero"]
    assert gpio.devices == []
    adapter.start()
    assert gpio.imports == ["gpiozero", sensors._FACTORIES[factory][0]]
    assert [device.pin for device in gpio.devices] == [27, 2, 17, 4, 3]
    assert all(device.pull_up is False and device.factory is gpio.factories[0] for device in gpio.devices)
    assert poll_at(adapter, clock, readings, 0.2) == SensorReading((0, 1, 0, 0, 1), 3, "ok", 0.2, True)
    gpio.fail_read_pin = 17
    assert poll_at(adapter, clock, readings, 0.21) == SensorReading((0, 1, 0, 0, 1), None, "fault", 0.2, False)
    adapter.stop()
    adapter.stop()
    assert all(device.close_count == 1 for device in gpio.devices)
    assert gpio.factories[0].close_count == 1
    assert poll_at(adapter, clock, readings, 0.4).sampled_at == 0.2


@pytest.mark.parametrize("opened", range(5))
def test_partial_startup_closes_every_created_resource(gpio, opened):
    gpio.fail_open_at = opened
    adapter = GPIOSensorAdapter(live_settings(), auto_timers=False)
    readings = []
    adapter.readingChanged.connect(readings.append)
    with pytest.raises(RuntimeError, match="input open failed"):
        adapter.start()
    assert readings == [SensorReading(None, None, "fault", None, False)]
    assert len(gpio.devices) == opened
    assert all(device.close_count == 1 for device in gpio.devices)
    assert gpio.factories[0].close_count == 1
    adapter.stop()
    assert gpio.factories[0].close_count == 1


def test_cleanup_attempts_all_resources_even_when_close_raises(gpio):
    adapter = GPIOSensorAdapter(live_settings(), auto_timers=False)
    adapter.start()
    gpio.fail_close_pin = 27
    gpio.fail_factory_close = True
    with pytest.raises(RuntimeError, match="input close failed; factory close failed"):
        adapter.stop()
    assert all(device.close_count == 1 for device in gpio.devices)
    assert gpio.factories[0].close_count == 1
    adapter.stop()
    assert gpio.factories[0].close_count == 1


def test_partial_startup_reports_original_and_cleanup_failure(gpio):
    gpio.fail_open_at = 2
    gpio.fail_close_pin = 27
    adapter = GPIOSensorAdapter(live_settings(), auto_timers=False)
    with pytest.raises(RuntimeError, match="input open failed; cleanup failed:.*input close failed"):
        adapter.start()
    assert all(device.close_count == 1 for device in gpio.devices)
    assert gpio.factories[0].close_count == 1
    adapter.stop()


def test_backend_initialization_failure_does_not_fallback(gpio):
    gpio.fail_factory = True
    adapter = GPIOSensorAdapter(live_settings(), auto_timers=False)
    with pytest.raises(RuntimeError, match="native: backend unavailable"):
        adapter.start()
    assert gpio.imports == ["gpiozero", "gpiozero.pins.native"]
    assert gpio.devices == []
    adapter.stop()


def test_unconfigured_backend_tries_only_allowed_hardware_factories(gpio):
    gpio.fail_factory = True
    adapter = GPIOSensorAdapter(live_settings(pin_factory=None), auto_timers=False)
    with pytest.raises(RuntimeError, match="Cannot initialize live GPIO backend"):
        adapter.start()
    assert gpio.imports == ["gpiozero"] + [entry[0] for entry in sensors._FACTORIES.values()]
    adapter.stop()


@pytest.mark.parametrize("name", ["mock", "custom", "gpiozero.pins.mock.MockFactory"])
def test_environment_cannot_silently_enable_mock(gpio, monkeypatch, name):
    monkeypatch.setenv("GPIOZERO_PIN_FACTORY", name)
    with pytest.raises(ConfigurationError, match="no mock backend"):
        GPIOSensorAdapter(live_settings(pin_factory=None), auto_timers=False)
    assert gpio.imports == []


def test_allowed_environment_backend_is_explicit(gpio, monkeypatch):
    monkeypatch.setenv("GPIOZERO_PIN_FACTORY", "lgpio")
    adapter = GPIOSensorAdapter(live_settings(pin_factory=None), auto_timers=False)
    adapter.start()
    adapter.stop()
    assert gpio.imports == ["gpiozero", "gpiozero.pins.lgpio"]


def test_configured_backend_takes_precedence_over_environment(gpio, monkeypatch):
    monkeypatch.setenv("GPIOZERO_PIN_FACTORY", "mock")
    adapter = GPIOSensorAdapter(live_settings(pin_factory="native"), auto_timers=False)
    adapter.start()
    adapter.stop()
    assert gpio.imports == ["gpiozero", "gpiozero.pins.native"]


def test_live_restart_reopens_resources(gpio):
    clock = Clock()
    adapter = GPIOSensorAdapter(live_settings(), clock=clock, auto_timers=False)
    readings = []
    adapter.readingChanged.connect(readings.append)
    adapter.start()
    poll_at(adapter, clock, readings, 0.2)
    adapter.stop()
    clock.now = 0.3
    adapter.start()
    assert readings[-1] == SensorReading((0, 1, 0, 0, 1), None, "unknown", 0.3, False)
    assert len(gpio.devices) == 10
    assert poll_at(adapter, clock, readings, 0.5).level == 3
    adapter.stop()
    assert all(device.close_count == 1 for device in gpio.devices)
    assert all(factory.close_count == 1 for factory in gpio.factories)
