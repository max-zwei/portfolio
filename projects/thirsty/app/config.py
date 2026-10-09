"""Strict local JSON schemas; no Qt or GPIO dependencies are imported here.

Device JSON mirrors DeviceSettings exactly: sensors, interaction and display.
Missing device sections/fields use documented dataclass defaults. Five pins and
wet_values are ordered bottom-to-top. None pins are deliberate unverified values;
validate_for_mode("live") rejects them before any GPIO package is imported.

Script JSON has REQUIRED sections copy, progress, water, refill, fault,
final_summary, repository_url. copy mirrors ScreenCopy, including required nonblank
start_title, start_body and start_prompt strings. progress is a nonempty
array of ScriptStep objects; the three incident sections are TranscriptRow
objects; final_summary is a nonempty array of output TranscriptRow objects.
Only progress rows carry delay_ms. IDs are globally unique. For example a row is
{"id": "backend", "type": "action", "variant": "running",
 "text": "Working on creating the backend", "delay_ms": 12000}.

repository_url MUST be an operator-provided absolute HTTP(S) URL. It has no
production default. Missing/blank/null URLs fail even in mock mode. Test fixture
URLs belong in explicitly labeled fixtures only. ConfigurationError messages
include the field path and load errors also include the file path.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
import json
from pathlib import Path
import re
from string import Formatter
from typing import Any, Mapping
from urllib.parse import urlsplit

from .contracts import MESSAGE_VARIANTS, Mode, RawBits, ScriptStep, TranscriptRow


class ConfigurationError(ValueError):
    """Operator-actionable invalid or unreadable application configuration."""


def _fail(path: str, message: str) -> None:
    raise ConfigurationError(f"{path}: {message}")


def _integer(value: Any, path: str, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:
        _fail(path, f"must be an integer from {low} through {high}")
    return value


def _boolean(value: Any, path: str) -> bool:
    if type(value) is not bool:
        _fail(path, "must be true or false")
    return value


def _text(value: Any, path: str, *, template: bool = False) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 16384:
        _fail(path, "must be a nonblank string of at most 16384 characters")
    if template:
        try:
            for _, field, spec, conversion in Formatter().parse(value):
                if field is not None and (field != "idea" or spec or conversion):
                    _fail(path, "only the literal {idea} substitution is allowed")
        except ValueError as exc:
            _fail(path, f"invalid message template: {exc}")
    return value


def _object(value: Any, path: str, allowed: set[str], required: set[str]) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    unknown = value.keys() - allowed
    if unknown:
        _fail(path, f"unknown field(s): {', '.join(sorted(unknown))}")
    missing = required - value.keys()
    if missing:
        _fail(path, f"missing required field(s): {', '.join(sorted(missing))}")
    return value


def _five(value: Any, path: str) -> tuple[Any, ...]:
    if not isinstance(value, (list, tuple)) or len(value) != 5:
        _fail(path, "must contain exactly five bottom-to-top entries")
    return tuple(value)


@dataclass(frozen=True, slots=True)
class SensorSettings:
    pins: tuple[int | None, ...] = (None, None, None, None, None)
    physical_pins: tuple[int | None, ...] = (None, None, None, None, None)
    wet_values: RawBits = (1, 1, 1, 1, 1)
    poll_interval_ms: int = 50
    stable_for_ms: int = 200
    stale_after_ms: int = 1000
    pin_factory: str | None = None
    hardware_verified: bool = False

    def __post_init__(self) -> None:
        for name, maximum in (("pins", 27), ("physical_pins", 40)):
            values = _five(getattr(self, name), f"sensors.{name}")
            assigned = []
            for index, value in enumerate(values):
                if value is not None:
                    assigned.append(_integer(value, f"sensors.{name}[{index}]", 0 if name == "pins" else 1, maximum))
            if len(set(assigned)) != len(assigned):
                _fail(f"sensors.{name}", "assigned pins must be distinct")
            object.__setattr__(self, name, values)
        wet = _five(self.wet_values, "sensors.wet_values")
        for index, value in enumerate(wet):
            _integer(value, f"sensors.wet_values[{index}]", 0, 1)
        object.__setattr__(self, "wet_values", wet)
        _integer(self.poll_interval_ms, "sensors.poll_interval_ms", 1, 60000)
        _integer(self.stable_for_ms, "sensors.stable_for_ms", 0, 60000)
        _integer(self.stale_after_ms, "sensors.stale_after_ms", self.poll_interval_ms, 3600000)
        if self.pin_factory not in (None, "lgpio", "rpigpio", "pigpio", "native"):
            _fail("sensors.pin_factory", "must be null, lgpio, rpigpio, pigpio or native")
        _boolean(self.hardware_verified, "sensors.hardware_verified")


@dataclass(frozen=True, slots=True)
class InteractionSettings:
    input_max_length: int = 500
    input_inactivity_ms: int = 120000
    finished_timeout_ms: int = 60000
    refill_hold_ms: int = 2000
    resume_level: int = 1

    def __post_init__(self) -> None:
        _integer(self.input_max_length, "interaction.input_max_length", 1, 10000)
        _integer(self.input_inactivity_ms, "interaction.input_inactivity_ms", 1, 86400000)
        _integer(self.finished_timeout_ms, "interaction.finished_timeout_ms", 1, 86400000)
        _integer(self.refill_hold_ms, "interaction.refill_hold_ms", 0, 86400000)
        _integer(self.resume_level, "interaction.resume_level", 1, 5)


@dataclass(frozen=True, slots=True)
class DisplaySettings:
    width: int = 1280
    height: int = 720
    fullscreen: bool = False

    def __post_init__(self) -> None:
        _integer(self.width, "display.width", 320, 7680)
        _integer(self.height, "display.height", 180, 4320)
        _boolean(self.fullscreen, "display.fullscreen")


@dataclass(frozen=True, slots=True)
class DeviceSettings:
    sensors: SensorSettings = SensorSettings()
    interaction: InteractionSettings = InteractionSettings()
    display: DisplaySettings = DisplaySettings()

    def __post_init__(self) -> None:
        for name, expected in (("sensors", SensorSettings), ("interaction", InteractionSettings), ("display", DisplaySettings)):
            if not isinstance(getattr(self, name), expected):
                _fail(name, f"must be {expected.__name__}")

    def validate_for_mode(self, mode: str | Mode) -> None:
        if mode not in (Mode.MOCK, Mode.LIVE):
            _fail("mode", "must be mock or live")
        if mode == Mode.LIVE and any(pin is None for pin in self.sensors.pins):
            _fail("sensors.pins", "live mode requires five configured, distinct BCM pins; calibrate the installation before launch")


@dataclass(frozen=True, slots=True)
class ScreenCopy:
    start_title: str
    start_body: str
    start_prompt: str
    input_title: str
    input_prompt: str
    input_placeholder: str
    input_submit_label: str
    empty_input_error: str
    long_input_error: str
    running_title: str
    finished_prompt: str
    repository_label: str
    water_label: str
    sensor_unknown_label: str
    sensor_fault_label: str

    def __post_init__(self) -> None:
        for field in fields(self):
            _text(getattr(self, field.name), f"copy.{field.name}")

    def as_qml(self) -> dict[str, str]:
        """QVariantMap values; key spelling intentionally matches the JSON."""
        return asdict(self)


def _validate_row(row: TranscriptRow | ScriptStep, path: str, *, step: bool = False) -> None:
    if not isinstance(row, ScriptStep if step else TranscriptRow):
        _fail(path, f"must be {'ScriptStep' if step else 'TranscriptRow'}")
    if not isinstance(row.id, str) or re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", row.id) is None:
        _fail(f"{path}.id", "must start with an ASCII letter and contain at most 64 letters, digits, underscores or hyphens")
    if not isinstance(row.type, str) or row.type not in MESSAGE_VARIANTS or row.type == "user":
        _fail(f"{path}.type", "must be task, action, error or output; user rows are controller-owned")
    if not isinstance(row.variant, str) or row.variant not in MESSAGE_VARIANTS[row.type]:
        _fail(f"{path}.variant", f"invalid variant for {row.type}; expected {', '.join(sorted(MESSAGE_VARIANTS[row.type]))}")
    _text(row.text, f"{path}.text", template=True)
    if step:
        _integer(row.delay_ms, f"{path}.delay_ms", 0, 3600000)


def _repository_url(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("repository_url", "an owner-provided app repository URL is required; configure it before launch (test URLs belong only in labeled fixtures)")
    if value != value.strip() or any(char.isspace() or ord(char) < 32 for char in value):
        _fail("repository_url", "must not contain whitespace or control characters")
    try:
        parts = urlsplit(value)
        port = parts.port
    except ValueError as exc:
        _fail("repository_url", f"invalid URL: {exc}")
    if parts.scheme not in ("https", "http") or not parts.hostname or parts.username is not None or parts.password is not None:
        _fail("repository_url", "must be an absolute HTTP(S) URL without credentials")
    if port is not None and not 1 <= port <= 65535:
        _fail("repository_url", "port must be from 1 through 65535")
    if any(char in value for char in '\\<>"{}|^`') or "\x7f" in value:
        _fail("repository_url", "contains characters that must be URL-encoded")
    if len(value) > 2048:
        _fail("repository_url", "must contain at most 2048 characters")
    return value


@dataclass(frozen=True, slots=True)
class ScriptConfig:
    copy: ScreenCopy
    progress: tuple[ScriptStep, ...]
    water: TranscriptRow
    refill: TranscriptRow
    fault: TranscriptRow
    final_summary: tuple[TranscriptRow, ...]
    repository_url: str

    def __post_init__(self) -> None:
        if not isinstance(self.copy, ScreenCopy):
            _fail("copy", "must be ScreenCopy")
        for name in ("progress", "final_summary"):
            rows = getattr(self, name)
            if not isinstance(rows, (list, tuple)) or not rows:
                _fail(name, "must be a nonempty array")
            object.__setattr__(self, name, tuple(rows))
        seen: set[str] = set()
        groups = [(f"progress[{index}]", row, True) for index, row in enumerate(self.progress)]
        groups.extend((name, getattr(self, name), False) for name in ("water", "refill", "fault"))
        groups.extend((f"final_summary[{index}]", row, False) for index, row in enumerate(self.final_summary))
        for path, row, step in groups:
            _validate_row(row, path, step=step)
            if row.id in seen:
                _fail(f"{path}.id", f"duplicate message ID {row.id!r}; IDs must be globally unique")
            seen.add(row.id)
            if path.startswith("final_summary") and row.type != "output":
                _fail(f"{path}.type", "final summary messages must use output")
        if (self.water.type, self.water.variant) != ("error", "water_level"):
            _fail("water", "must use type=error and variant=water_level")
        if (self.fault.type, self.fault.variant) != ("action", "error"):
            _fail("fault", "must use type=action and variant=error")
        if (self.refill.type, self.refill.variant) != ("action", "running"):
            _fail("refill", "must use type=action and variant=running")
        _repository_url(self.repository_url)


def parse_device(value: Any) -> DeviceSettings:
    root = _object(value, "device", {"sensors", "interaction", "display"}, set())
    sections: dict[str, Any] = {}
    for name, cls in (("sensors", SensorSettings), ("interaction", InteractionSettings), ("display", DisplaySettings)):
        section = _object(root.get(name, {}), name, {field.name for field in fields(cls)}, set())
        sections[name] = cls(**section)
    return DeviceSettings(**sections)


def _parse_row(value: Any, path: str, *, step: bool = False) -> TranscriptRow | ScriptStep:
    keys = {"id", "type", "variant", "text"} | ({"delay_ms"} if step else set())
    row = _object(value, path, keys, keys)
    return ScriptStep(**row) if step else TranscriptRow(**row)


def parse_script(value: Any) -> ScriptConfig:
    keys = {"copy", "progress", "water", "refill", "fault", "final_summary", "repository_url"}
    root = _object(value, "script", keys, keys - {"repository_url"})
    # Deliberately report the missing destination before less important copy errors.
    repository_url = _repository_url(root.get("repository_url"))
    copy_keys = {field.name for field in fields(ScreenCopy)}
    copy = ScreenCopy(**_object(root["copy"], "copy", copy_keys, copy_keys))
    groups: dict[str, tuple[Any, ...]] = {}
    for name in ("progress", "final_summary"):
        rows = root[name]
        if not isinstance(rows, list) or not rows:
            _fail(name, "must be a nonempty array")
        groups[name] = tuple(_parse_row(row, f"{name}[{index}]", step=name == "progress") for index, row in enumerate(rows))
    return ScriptConfig(
        copy=copy,
        progress=groups["progress"],
        water=_parse_row(root["water"], "water"),
        refill=_parse_row(root["refill"], "refill"),
        fault=_parse_row(root["fault"], "fault"),
        final_summary=groups["final_summary"],
        repository_url=repository_url,
    )


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("JSON", f"duplicate field {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    _fail("JSON", f"non-finite number {value} is not valid JSON")


def _load(path: str | Path, parser: Any) -> Any:
    source = Path(path)
    try:
        with source.open(encoding="utf-8") as stream:
            value = json.load(stream, object_pairs_hook=_reject_duplicate_keys, parse_constant=_reject_constant)
        return parser(value)
    except (OSError, UnicodeError, json.JSONDecodeError, ConfigurationError) as exc:
        raise ConfigurationError(f"{source}: {exc}") from exc


def load_device(path: str | Path) -> DeviceSettings:
    return _load(path, parse_device)


def load_script(path: str | Path) -> ScriptConfig:
    return _load(path, parse_script)
