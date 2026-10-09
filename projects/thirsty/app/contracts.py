"""Shared, Qt-independent data and event contracts for thirsty.

All timestamps are seconds from the same injected monotonic clock. No component
uses wall-clock time. JSON settings use snake_case; Qt properties and slots use
exactly the camelCase names below. The controller owns all session mutation on
the Qt thread; sensor signals crossing threads must use a queued connection.

Controller implementation contract (app.controller.ExperienceController)::

    ExperienceController(settings: DeviceSettings, script: ScriptConfig, *,
                         clock: Callable[[], float] = time.monotonic,
                         auto_timers: bool = True, parent: QObject | None = None)

Slots: start(), submit(text: str), reset(), activity(), receiveReading(object),
       tick(). tick() advances every deadline using clock(), never a tick count.
       Tests inject a fake clock, set auto_timers=False, deliver readings, then
       call tick(); they never sleep. At coincident deadlines, sensing validity
       and interruptions MUST be checked before progress/completion.
Properties (with individual <property>Changed notify signals):
    state: str; waterLevel: QVariant (int 0..5 or None); sensorStatus: str;
    transcript: QAbstractListModel (constant); idea: str; validationError: str;
    copy: QVariantMap (constant); repositoryUrl: str (constant);
    qrSource: str (notify qrSourceChanged).
The transcript uses standard rowsInserted/modelReset signals, not a parallel
transcriptChanged signal. Role names are EXACTLY id, type, variant, text, assigned
consecutively from Qt.UserRole + 1. IDs do not change after insertion. Script IDs
are prefixed `progress:` / `summary:`; visitor ID is `visitor:idea`; interruption
IDs use `water:<incident>`, `fault:<incident>`, `refill:<incident>`. Repeated sensor
heartbeats must not create additional rows for one incident. No snake_case Qt
signal aliases are provided: use stateChanged/waterLevelChanged/etc. consistently.
QML context property name is `controller`. copy exposes ScreenCopy field names
(snake_case) verbatim. Plain text only: QML must never interpret visitor text as
rich text. Script interpolation permits only the literal token {idea}.

Sensor implementation contract (app.sensors):
    MockSensorAdapter(settings: SensorSettings, *, clock=time.monotonic,
                      auto_timers=True, parent=None)
    GPIOSensorAdapter(settings: SensorSettings, *, clock=time.monotonic,
                      auto_timers=True, parent=None)
Both expose readingChanged = Signal(object), start(), stop(), poll(). Each poll
emits a SensorReading heartbeat even if unchanged. Mock exposes setRawBits(bits)
and setReadFailure(failed: bool), and starts unreadable, never with a full tank.
GPIO Zero is imported only when constructing the live adapter; missing packages,
pins or backend errors never select mock mode. stop() releases GPIO resources.

SensorReading.raw_bits is the latest successful physical bottom-to-top read;
level is the LAST ACCEPTED stabilized level (not a count of the latest raw bits).
Raw and accepted values can differ during the debounce window. is_stable=False
marks this uncertainty; it prevents progress and breaks a refill/recovery hold.
sampled_at is the last successful RAW read, including unstable reads, not the
last level change. A read failure retains that timestamp; before any successful
read it is None. Unknown/fault readings have level=None. is_stable=True alone
never establishes validity: status, level and freshness must also be checked.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from typing import Literal, TypeAlias

RawBits: TypeAlias = tuple[int, int, int, int, int]
SensorStatus: TypeAlias = Literal["unknown", "ok", "fault"]
SessionState: TypeAlias = Literal[
    "start", "input", "running", "paused_water", "paused_sensor", "finished"
]
MessageType: TypeAlias = Literal["task", "action", "error", "output", "user"]
MessageVariant: TypeAlias = Literal["H1", "body", "running", "error", "water_level"]

SENSOR_COUNT = 5
TRANSCRIPT_ROLES = ("id", "type", "variant", "text")
MESSAGE_VARIANTS: dict[str, frozenset[str]] = {
    "task": frozenset({"H1", "body"}),
    "action": frozenset({"running", "error"}),
    "error": frozenset({"water_level"}),
    "output": frozenset({"H1", "body"}),
    "user": frozenset({"body"}),
}


class Mode(str, Enum):
    MOCK = "mock"
    LIVE = "live"


@dataclass(frozen=True, slots=True)
class SensorReading:
    raw_bits: RawBits | None
    level: int | None
    status: SensorStatus
    sampled_at: float | None
    is_stable: bool = True

    def __post_init__(self) -> None:
        if self.raw_bits is not None and (
            not isinstance(self.raw_bits, tuple)
            or len(self.raw_bits) != SENSOR_COUNT
            or any(type(bit) is not int or bit not in (0, 1) for bit in self.raw_bits)
        ):
            raise ValueError("raw_bits must be a bottom-to-top tuple of five 0/1 integers or None")
        if self.status not in ("unknown", "ok", "fault"):
            raise ValueError("status must be unknown, ok or fault")
        if self.level is not None and (type(self.level) is not int or not 0 <= self.level <= 5):
            raise ValueError("level must be an integer from 0 through 5 or None")
        if (self.status == "ok") != (self.level is not None):
            raise ValueError("only status=ok may provide a level; ok requires a level")
        if self.sampled_at is not None and (
            type(self.sampled_at) not in (int, float)
            or not math.isfinite(self.sampled_at)
            or self.sampled_at < 0
        ):
            raise ValueError("sampled_at must be finite nonnegative monotonic seconds or None")
        if self.raw_bits is not None and self.sampled_at is None:
            raise ValueError("a successful raw reading requires sampled_at")
        if self.status == "ok" and self.raw_bits is None:
            raise ValueError("status=ok requires a successful raw reading")
        if type(self.is_stable) is not bool:
            raise ValueError("is_stable must be a boolean")


@dataclass(frozen=True, slots=True)
class TranscriptRow:
    id: str
    type: MessageType
    variant: MessageVariant
    text: str


@dataclass(frozen=True, slots=True)
class ScriptStep:
    id: str
    type: MessageType
    variant: MessageVariant
    text: str
    delay_ms: int
