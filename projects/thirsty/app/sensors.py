"""Qt-thread polling of bottom-to-top switches; no GPIO callbacks or sleeps.

A successful poll always refreshes sampled_at, even during debounce. Unreadable
mock input is unknown immediately; read errors are fault until the last success
expires, then unknown. Neither path fabricates a new successful timestamp.
start() polls immediately and is idempotent; stop() publishes unknown, stops the
Qt timer and releases live resources. Explicit poll() while stopped only emits
unknown. A restart requires a new stable window, including after a stale gap.
"""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
import os
import time
from typing import cast

from PySide6.QtCore import QObject, Qt, QTimer, Signal, Slot

from .config import ConfigurationError, SensorSettings
from .contracts import RawBits, SensorReading, SensorStatus


_FACTORIES = {
    "lgpio": ("gpiozero.pins.lgpio", "LGPIOFactory"),
    "rpigpio": ("gpiozero.pins.rpigpio", "RPiGPIOFactory"),
    "pigpio": ("gpiozero.pins.pigpio", "PiGPIOFactory"),
    "native": ("gpiozero.pins.native", "NativeFactory"),
}


class _SensorAdapter(QObject):
    readingChanged = Signal(object)

    def __init__(self, settings: SensorSettings, *, clock: Callable[[], float] = time.monotonic,
                 auto_timers: bool = True, parent: QObject | None = None):
        super().__init__(parent)
        self._settings = settings
        self._clock = clock
        self._auto_timers = auto_timers
        self._running = False
        self._raw_bits: RawBits | None = None
        self._sampled_at: float | None = None
        self._candidate: RawBits | None = None
        self._candidate_deadline = 0.0
        self._level: int | None = None
        self._status: SensorStatus = "unknown"
        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.setInterval(settings.poll_interval_ms)
        self._timer.timeout.connect(self.poll)

    def _open(self) -> None:
        pass

    def _close(self) -> None:
        pass

    def _read_raw(self) -> RawBits | None:
        raise NotImplementedError

    def _invalidate(self, status: SensorStatus) -> None:
        self._candidate = None
        self._level = None
        self._status = status

    def _emit(self, stable: bool) -> None:
        self.readingChanged.emit(SensorReading(
            self._raw_bits, self._level, self._status, self._sampled_at, stable,
        ))

    def _stale(self, now: float) -> bool:
        return (self._sampled_at is not None
                and now >= self._sampled_at + self._settings.stale_after_ms / 1000)

    @Slot()
    def start(self) -> None:
        if self._running:
            return
        self._raw_bits = None
        self._sampled_at = None
        self._invalidate("unknown")
        try:
            self._open()
        except Exception:
            self._invalidate("fault")
            self._emit(False)
            raise
        self._running = True
        self.poll()
        if self._auto_timers and self._running:
            self._timer.start()

    @Slot()
    def stop(self) -> None:
        was_running = self._running
        self._running = False
        self._timer.stop()
        self._invalidate("unknown")
        try:
            self._close()
        finally:
            if was_running:
                self._emit(False)

    @Slot()
    def poll(self) -> None:
        if not self._running:
            self._invalidate("unknown")
            self._emit(False)
            return
        if self._stale(self._clock()):
            self._invalidate("unknown")
        try:
            bits = self._read_raw()
        except Exception:
            self._invalidate("unknown" if self._stale(self._clock()) else "fault")
            self._emit(False)
            return
        if bits is None:
            self._invalidate("unknown")
            self._emit(False)
            return
        now = self._clock()
        self._raw_bits = bits
        self._sampled_at = now
        if bits != self._candidate:
            self._candidate = bits
            self._candidate_deadline = now + self._settings.stable_for_ms / 1000
        stable = now >= self._candidate_deadline
        if stable:
            # Only a wet prefix is a physical level, never an isolated wet bit.
            level = 0
            dry_seen = False
            for bit, wet_value in zip(bits, self._settings.wet_values):
                if bit == wet_value:
                    if dry_seen:
                        self._level = None
                        self._status = "fault"
                        break
                    level += 1
                else:
                    dry_seen = True
            else:
                self._level = level
                self._status = "ok"
        self._emit(stable)


class MockSensorAdapter(_SensorAdapter):
    """External mock drivers set input, then normal Qt polling publishes it."""

    def __init__(self, settings: SensorSettings, *, clock: Callable[[], float] = time.monotonic,
                 auto_timers: bool = True, parent: QObject | None = None):
        super().__init__(settings, clock=clock, auto_timers=auto_timers, parent=parent)
        self._input_bits: RawBits | None = None
        self._read_failure = False

    @Slot(object)
    def setRawBits(self, bits: RawBits | list[int] | None) -> None:
        if bits is not None:
            if (not isinstance(bits, (tuple, list)) or len(bits) != 5
                    or any(type(bit) is not int or bit not in (0, 1) for bit in bits)):
                raise ValueError("mock raw bits must be five bottom-to-top 0/1 integers or None")
            bits = cast(RawBits, tuple(bits))
        self._input_bits = bits

    @Slot(bool)
    def setReadFailure(self, failed: bool) -> None:
        if type(failed) is not bool:
            raise ValueError("mock read failure must be a boolean")
        self._read_failure = failed

    def _read_raw(self) -> RawBits | None:
        if self._read_failure:
            raise OSError("mock sensor read failure")
        return self._input_bits


class GPIOSensorAdapter(_SensorAdapter):
    """Own GPIO Zero devices and their hardware factory, sampled only by Qt.

    An explicit configured/environment backend must succeed; it never falls
    back. With neither specified, try GPIO Zero's normal hardware backend order.
    Mock/custom factories are deliberately excluded, including environment ones.
    """

    def __init__(self, settings: SensorSettings, *, clock: Callable[[], float] = time.monotonic,
                 auto_timers: bool = True, parent: QObject | None = None):
        if any(pin is None for pin in settings.pins) or len(set(settings.pins)) != 5:
            raise ConfigurationError("sensors.pins: live mode requires five configured, distinct BCM pins")
        factory_name = settings.pin_factory or os.environ.get("GPIOZERO_PIN_FACTORY")
        if factory_name is not None and factory_name not in _FACTORIES:
            raise ConfigurationError("sensors.pin_factory: live mode requires lgpio, rpigpio, pigpio or native; no mock backend")
        super().__init__(settings, clock=clock, auto_timers=auto_timers, parent=parent)
        try:
            self._device_class = import_module("gpiozero").DigitalInputDevice
        except ImportError as exc:
            raise RuntimeError("Live sensors require the packaged GPIO Zero dependency") from exc
        self._factory_name = factory_name
        self._factory = None
        self._devices = []

    def _open(self) -> None:
        names = (self._factory_name,) if self._factory_name is not None else tuple(_FACTORIES)
        failures = []
        for name in names:
            module, class_name = _FACTORIES[name]
            try:
                self._factory = getattr(import_module(module), class_name)()
                break
            except Exception as exc:
                failures.append(f"{name}: {exc}")
        if self._factory is None:
            raise RuntimeError("Cannot initialize live GPIO backend: " + "; ".join(failures))
        try:
            for pin in self._settings.pins:
                self._devices.append(self._device_class(pin, pull_up=False, pin_factory=self._factory))
        except Exception as exc:
            try:
                self._close()
            except Exception as cleanup_error:
                raise RuntimeError(f"Cannot open GPIO inputs: {exc}; cleanup failed: {cleanup_error}") from exc
            raise RuntimeError(f"Cannot open GPIO inputs: {exc}") from exc

    def _read_raw(self) -> RawBits:
        # DigitalInputDevice.value is physical 0/1 with pull_up=False. Reading
        # these properties here avoids GPIO callback threads touching consumers.
        return cast(RawBits, tuple(int(device.value) for device in self._devices))

    def _close(self) -> None:
        devices, self._devices = self._devices, []
        factory, self._factory = self._factory, None
        errors = []
        for resource in (*devices, factory):
            if resource is not None:
                try:
                    resource.close()
                except Exception as exc:
                    errors.append(str(exc))
        if errors:
            raise RuntimeError("Cannot release GPIO resources: " + "; ".join(errors))
