"""In-memory, Qt-thread experience state and monotonic script scheduling."""

from __future__ import annotations

from collections.abc import Callable
import re
import time

from PySide6.QtCore import (
    QAbstractListModel, QModelIndex, QObject, Property, QThread, QTimer, Qt,
    Signal, Slot,
)

from .config import DeviceSettings, ScriptConfig
from .contracts import SensorReading, ScriptStep, TranscriptRow, TRANSCRIPT_ROLES


class TranscriptModel(QAbstractListModel):
    """Append-only session rows with the exact roles consumed by QML."""

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._rows: list[TranscriptRow] = []
        self._roles = {
            int(Qt.ItemDataRole.UserRole) + index + 1: name.encode("ascii")
            for index, name in enumerate(TRANSCRIPT_ROLES)
        }

    def roleNames(self) -> dict[int, bytes]:
        return self._roles

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.column() != 0 or not 0 <= index.row() < len(self._rows):
            return None
        field = int(role) - int(Qt.ItemDataRole.UserRole) - 1
        if not 0 <= field < len(TRANSCRIPT_ROLES):
            return None
        return getattr(self._rows[index.row()], TRANSCRIPT_ROLES[field])

    def append(self, row: TranscriptRow) -> None:
        position = len(self._rows)
        self.beginInsertRows(QModelIndex(), position, position)
        self._rows.append(row)
        self.endInsertRows()

    def clear(self) -> None:
        if self._rows:
            self.beginResetModel()
            self._rows.clear()
            self.endResetModel()


class ExperienceController(QObject):
    stateChanged = Signal()
    waterLevelChanged = Signal()
    sensorStatusChanged = Signal()
    ideaChanged = Signal()
    validationErrorChanged = Signal()
    qrSourceChanged = Signal()

    def __init__(
        self,
        settings: DeviceSettings,
        script: ScriptConfig,
        *,
        clock: Callable[[], float] = time.monotonic,
        auto_timers: bool = True,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._settings = settings
        self._script = script
        self._clock = clock
        self._copy = script.copy.as_qml()
        self._transcript = TranscriptModel(self)
        self._state = "start"
        self._water_level: int | None = None
        self._sensor_status = "unknown"
        self._idea = ""
        self._validation_error = ""
        self._qr_source = ""
        self._reading: SensorReading | None = None
        self._reading_floor = clock()
        self._next_step = 0
        self._step_deadline: int | None = None
        self._remaining_delay = 0
        self._input_deadline: int | None = None
        self._finished_deadline: int | None = None
        self._refill_since: int | None = None
        self._incident = 0
        self._incident_kinds: set[str] = set()
        # One owned timer drives every deadline, including sensing freshness.
        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.setInterval(min(settings.sensors.poll_interval_ms, 50))
        self._timer.timeout.connect(self.tick)
        if auto_timers:
            self._timer.start()

    @Property(str, notify=stateChanged)
    def state(self) -> str:
        return self._state

    @Property("QVariant", notify=waterLevelChanged)
    def waterLevel(self) -> int | None:
        return self._water_level

    @Property(str, notify=sensorStatusChanged)
    def sensorStatus(self) -> str:
        return self._sensor_status

    @Property(QObject, constant=True)
    def transcript(self) -> TranscriptModel:
        return self._transcript

    @Property(str, notify=ideaChanged)
    def idea(self) -> str:
        return self._idea

    @Property(str, notify=validationErrorChanged)
    def validationError(self) -> str:
        return self._validation_error

    @Property("QVariantMap", constant=True)
    def copy(self) -> dict[str, str]:
        return self._copy

    @Property(str, constant=True)
    def repositoryUrl(self) -> str:
        return self._script.repository_url

    @Property(str, notify=qrSourceChanged)
    def qrSource(self) -> str:
        return self._qr_source

    @qrSource.setter
    def qrSource(self, source: str) -> None:
        self.setQrSource(source)

    @Slot(str)
    def setQrSource(self, source: str) -> None:
        self._assert_thread()
        self._change("_qr_source", source, self.qrSourceChanged)

    def _now_ns(self) -> int:
        # Normalize the injected seconds clock once, before doing arithmetic.
        # Integer nanoseconds keep fractional-second deadlines exact without
        # tolerances that could commit a stage before its deadline.
        return round(self._clock() * 1_000_000_000)

    def _assert_thread(self) -> None:
        if QThread.currentThread() != self.thread():
            raise RuntimeError("ExperienceController must be called on its Qt thread")

    def _change(self, name: str, value, signal) -> None:
        if getattr(self, name) != value:
            setattr(self, name, value)
            signal.emit()

    def _set_state(self, state: str) -> None:
        self._change("_state", state, self.stateChanged)

    @Slot()
    def start(self) -> None:
        self._assert_thread()
        if self._state != "start":
            return
        self._input_deadline = self._now_ns() + self._settings.interaction.input_inactivity_ms * 1_000_000
        self._set_state("input")

    @Slot()
    def activity(self) -> None:
        self._assert_thread()
        now = self._now_ns()
        if self._state != "input":
            return
        if self._input_deadline is not None and now >= self._input_deadline:
            self.reset()
            return
        self._input_deadline = now + self._settings.interaction.input_inactivity_ms * 1_000_000

    @Slot(str)
    def submit(self, text: str) -> None:
        self._assert_thread()
        if self._state != "input":
            return
        self.activity()
        if self._state != "input":
            return
        idea = re.sub(r"[\r\n\v\f\x85\u2028\u2029]+", " ", text).strip()
        if not idea:
            self._change("_validation_error", self._script.copy.empty_input_error, self.validationErrorChanged)
            return
        if len(idea) > self._settings.interaction.input_max_length:
            self._change("_validation_error", self._script.copy.long_input_error, self.validationErrorChanged)
            return
        self._change("_validation_error", "", self.validationErrorChanged)
        self._change("_idea", idea, self.ideaChanged)
        self._input_deadline = None
        self._transcript.append(TranscriptRow("visitor:idea", "user", "body", idea))
        self._remaining_delay = self._script.progress[0].delay_ms * 1_000_000
        self._step_deadline = self._now_ns() + self._remaining_delay
        self._set_state("running")
        self.tick()

    @Slot()
    def reset(self) -> None:
        self._assert_thread()
        self._reading_floor = self._clock()
        self._reading = None
        self._next_step = 0
        self._step_deadline = None
        self._remaining_delay = 0
        self._input_deadline = None
        self._finished_deadline = None
        self._refill_since = None
        self._incident = 0
        self._incident_kinds.clear()
        self._change("_idea", "", self.ideaChanged)
        self._change("_validation_error", "", self.validationErrorChanged)
        self._change("_water_level", None, self.waterLevelChanged)
        self._change("_sensor_status", "unknown", self.sensorStatusChanged)
        self._transcript.clear()
        self._set_state("start")

    @Slot(object)
    def receiveReading(self, reading: SensorReading) -> None:
        self._assert_thread()
        if not isinstance(reading, SensorReading):
            raise TypeError("receiveReading expects SensorReading")
        now = self._clock()
        if reading.sampled_at is not None:
            if reading.sampled_at < self._reading_floor or reading.sampled_at > now:
                return
            if (self._reading is not None and self._reading.sampled_at is not None
                    and reading.sampled_at < self._reading.sampled_at):
                return
        now = round(now * 1_000_000_000)
        # A fresh heartbeat cannot conceal an unobserved stale interval. Check
        # only safety here: never commit a due step using the superseded sample.
        if self._reading is not None and not self._fresh(now):
            self._update_sensor(now)
            self._guard_progress(now)
        self._reading = reading
        self.tick()

    def _fresh(self, now: int) -> bool:
        sampled = self._reading.sampled_at if self._reading is not None else None
        return (
            sampled is not None
            and 0 <= now - round(sampled * 1_000_000_000)
            <= self._settings.sensors.stale_after_ms * 1_000_000
        )

    def _update_sensor(self, now: int) -> None:
        reading = self._reading
        # Explicit failures stay faults even when their last good sample ages.
        status = "fault" if reading is not None and reading.status == "fault" else "unknown"
        if reading is not None and reading.status == "ok" and self._fresh(now):
            status = "ok"
        level = reading.level if reading is not None and status == "ok" else None
        self._change("_water_level", level, self.waterLevelChanged)
        self._change("_sensor_status", status, self.sensorStatusChanged)

    def _freeze(self, now: int) -> None:
        if self._step_deadline is not None:
            self._remaining_delay = max(0, self._step_deadline - now)
            self._step_deadline = None

    def _append_template(self, row: TranscriptRow | ScriptStep, identifier: str) -> None:
        self._transcript.append(TranscriptRow(
            identifier, row.type, row.variant, row.text.replace("{idea}", self._idea),
        ))

    def _pause(self, kind: str, now: int) -> None:
        self._freeze(now)
        self._refill_since = None
        if self._state == "running":
            self._incident += 1
            self._incident_kinds.clear()
        self._set_state("paused_water" if kind == "water" else "paused_sensor")
        if kind not in self._incident_kinds:
            self._incident_kinds.add(kind)
            self._append_template(getattr(self._script, kind), f"{kind}:{self._incident}")

    def _guard_progress(self, now: int) -> bool:
        if self._state not in ("running", "paused_water", "paused_sensor"):
            return False
        if self._sensor_status != "ok":
            freeze_at = now
            if self._reading is not None and self._reading.sampled_at is not None and not self._fresh(now):
                freeze_at = min(
                    now,
                    round(self._reading.sampled_at * 1_000_000_000)
                    + self._settings.sensors.stale_after_ms * 1_000_000,
                )
            self._pause("fault", freeze_at)
            return False
        if self._reading is None or not self._reading.is_stable:
            # A debounce candidate is not an accepted fault or empty tank.
            self._freeze(now)
            self._refill_since = None
            return False
        if self._water_level == 0:
            self._pause("water", now)
            return False
        if self._state != "running":
            if self._water_level < self._settings.interaction.resume_level:
                self._refill_since = None
                return False
            if self._refill_since is None:
                self._refill_since = now
            if now < self._refill_since + self._settings.interaction.refill_hold_ms * 1_000_000:
                return False
            self._refill_since = None
            self._append_template(self._script.refill, f"refill:{self._incident}")
            self._set_state("running")
        if self._step_deadline is None:
            self._step_deadline = now + self._remaining_delay
        return True

    @Slot()
    def tick(self) -> None:
        self._assert_thread()
        now = self._now_ns()
        self._update_sensor(now)
        if self._state == "input" and self._input_deadline is not None and now >= self._input_deadline:
            self.reset()
            return
        if self._state == "finished" and self._finished_deadline is not None and now >= self._finished_deadline:
            self.reset()
            return
        if not self._guard_progress(now):
            return
        while self._step_deadline is not None and now >= self._step_deadline:
            step = self._script.progress[self._next_step]
            self._append_template(step, f"progress:{step.id}")
            self._next_step += 1
            if self._next_step == len(self._script.progress):
                self._step_deadline = None
                self._remaining_delay = 0
                for row in self._script.final_summary:
                    self._append_template(row, f"summary:{row.id}")
                self._finished_deadline = now + self._settings.interaction.finished_timeout_ms * 1_000_000
                self._set_state("finished")
                return
            self._step_deadline += self._script.progress[self._next_step].delay_ms * 1_000_000
