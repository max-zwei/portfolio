"""Controller-only fixtures: synthetic copy, fake monotonic time, no GPIO."""

from dataclasses import dataclass, fields, replace

import pytest
from PySide6.QtCore import QCoreApplication, QModelIndex, Qt
from PySide6.QtQml import QQmlContext, QQmlEngine, QQmlExpression

from app.config import DeviceSettings, InteractionSettings, ScreenCopy, ScriptConfig
from app.contracts import SensorReading, ScriptStep, TranscriptRow, TRANSCRIPT_ROLES
from app.controller import ExperienceController


@pytest.fixture(scope="session")
def qt_application():
    application = QCoreApplication.instance() or QCoreApplication([])
    yield application


class FakeClock:
    def __init__(self):
        self.milliseconds = 0

    def __call__(self):
        return self.milliseconds / 1000

    def advance(self, milliseconds):
        self.milliseconds += milliseconds


def script_fixture(delays=(1000, 1500, 2000)):
    """TEST FIXTURE ONLY; not the recorded visitor-facing PocketPlan script."""
    return ScriptConfig(
        copy=ScreenCopy(**{field.name: f"Fixture {field.name}" for field in fields(ScreenCopy)}),
        progress=tuple(
            ScriptStep(f"step-{index}", "action", "running", f"Stage {index}: {{idea}}", delay)
            for index, delay in enumerate(delays)
        ),
        water=TranscriptRow("water", "error", "water_level", "Fixture refill request"),
        refill=TranscriptRow("refill", "action", "running", "Fixture resuming"),
        fault=TranscriptRow("fault", "action", "error", "Fixture sensor problem"),
        final_summary=(
            TranscriptRow("heading", "output", "H1", "Fixture result"),
            TranscriptRow("body", "output", "body", "Result for {idea}"),
        ),
        repository_url="https://example.org/controller-test-fixture",
    )


def model_rows(controller):
    model = controller.transcript
    return [
        {
            name: model.data(model.index(index, 0), int(Qt.ItemDataRole.UserRole) + role + 1)
            for role, name in enumerate(TRANSCRIPT_ROLES)
        }
        for index in range(model.rowCount())
    ]


def ids(controller, prefix=""):
    return [row["id"] for row in model_rows(controller) if row["id"].startswith(prefix)]


@dataclass
class Rig:
    controller: ExperienceController
    clock: FakeClock
    level: int | None = 5
    status: str = "ok"
    stable: bool = True

    def send(self, level=5, *, status="ok", stable=True):
        self.level, self.status, self.stable = level, status, stable
        bits = tuple(int(index < level) for index in range(5)) if level is not None else None
        self.controller.receiveReading(SensorReading(bits, level, status, self.clock(), stable))

    def advance(self, milliseconds):
        """Maintain physical heartbeats, independently of accepted level changes."""
        while milliseconds:
            delta = min(milliseconds, 250)
            self.clock.advance(delta)
            self.send(self.level, status=self.status, stable=self.stable)
            self.controller.tick()
            milliseconds -= delta

    def begin(self, idea="Fixture idea"):
        self.send()
        self.controller.start()
        self.controller.submit(idea)

    def recover(self, level=1):
        self.send(level)
        self.advance(2000)


@pytest.fixture
def make_rig(qt_application):
    controllers = []

    def make(*, delays=(1000, 1500, 2000), settings=None):
        clock = FakeClock()
        controller = ExperienceController(
            settings or DeviceSettings(), script_fixture(delays), clock=clock, auto_timers=False,
        )
        controllers.append(controller)
        return Rig(controller, clock)

    yield make
    for controller in controllers:
        controller.deleteLater()


@pytest.mark.parametrize("step_index", range(3))
@pytest.mark.parametrize("at_boundary", [False, True])
@pytest.mark.parametrize("interruption", ["water", "fault", "unknown"])
def test_interrupt_every_step_and_final_boundary(make_rig, step_index, at_boundary, interruption):
    rig = make_rig()
    controller = rig.controller
    rig.begin()
    delays = (1000, 1500, 2000)
    rig.advance(sum(delays[:step_index]))
    assert len(ids(controller, "progress:")) == step_index
    elapsed = delays[step_index] if at_boundary else delays[step_index] // 2
    # Jump only the last interval so a due heartbeat cannot commit the step
    # before the interruption arrives at exactly that deadline.
    rig.advance(max(0, elapsed - 250))
    rig.clock.advance(min(elapsed, 250))
    if interruption == "water":
        rig.send(0)
        assert controller.state == "paused_water"
    else:
        rig.send(None, status=interruption)
        assert controller.state == "paused_sensor"
    assert len(ids(controller, "progress:")) == step_index
    assert not ids(controller, "summary:")
    rig.advance(5000)
    assert len(ids(controller, "progress:")) == step_index
    rig.send(1)
    rig.advance(1999)
    assert controller.state.startswith("paused_")
    assert len(ids(controller, "progress:")) == step_index
    rig.advance(1)
    remaining = delays[step_index] - elapsed
    if remaining:
        assert controller.state == "running"
        rig.advance(remaining - 1)
        assert len(ids(controller, "progress:")) == step_index
        rig.advance(1)
    assert len(ids(controller, "progress:")) == step_index + 1
    assert ids(controller, "refill:") == ["refill:1"]
    rig.advance(sum(delays[step_index + 1:]))
    assert controller.state == "finished"
    assert ids(controller, "progress:") == [f"progress:step-{index}" for index in range(3)]
    assert ids(controller, "summary:") == ["summary:heading", "summary:body"]
    rig.advance(5000)
    assert len(set(ids(controller))) == len(ids(controller))


@pytest.mark.parametrize("status,level,state", [
    ("ok", 0, "paused_water"), ("unknown", None, "paused_sensor"), ("fault", None, "paused_sensor"),
])
def test_dry_unknown_fault_start_cannot_emit_zero_delay_progress(make_rig, status, level, state):
    rig = make_rig(delays=(0, 1000))
    rig.send(level, status=status)
    rig.controller.start()
    rig.controller.submit("A visitor idea")
    assert rig.controller.state == state
    assert not ids(rig.controller, "progress:")
    rig.recover()
    assert ids(rig.controller, "progress:") == ["progress:step-0"]
    rig.advance(1000)
    assert rig.controller.state == "finished"


def test_no_reading_start_is_unknown_not_assumed_full(make_rig):
    rig = make_rig(delays=(0,))
    controller = rig.controller
    assert controller.waterLevel is None
    assert controller.sensorStatus == "unknown"
    controller.start()
    controller.submit("Idea")
    assert controller.state == "paused_sensor"
    assert ids(controller) == ["visitor:idea", "fault:1"]


def test_repeated_refills_keep_pending_delay_and_never_duplicate_rows(make_rig):
    rig = make_rig(delays=(1000,))
    rig.begin()
    for incident in range(1, 4):
        rig.advance(100)
        rig.send(0)
        rig.advance(3000)
        rig.recover()
        assert rig.controller.state == "running"
        assert ids(rig.controller, "water:") == [f"water:{index}" for index in range(1, incident + 1)]
        assert ids(rig.controller, "refill:") == [f"refill:{index}" for index in range(1, incident + 1)]
    rig.advance(699)
    assert not ids(rig.controller, "progress:")
    rig.advance(1)
    assert rig.controller.state == "finished"
    assert len(set(ids(rig.controller))) == len(ids(rig.controller))


def test_pause_kind_changes_have_one_message_each_per_incident(make_rig):
    rig = make_rig()
    rig.begin()
    rig.send(0)
    for _ in range(3):
        rig.send(None, status="fault")
        assert rig.controller.state == "paused_sensor"
        rig.send(0)
        assert rig.controller.state == "paused_water"
    assert ids(rig.controller) == ["visitor:idea", "water:1", "fault:1"]
    rig.recover()
    assert ids(rig.controller, "refill:") == ["refill:1"]


def test_unchanged_and_rising_positive_heartbeats_preserve_hold(make_rig):
    rig = make_rig(delays=(1000,))
    rig.begin()
    rig.send(0)
    rig.send(1)
    rig.advance(750)
    rig.send(2)
    rig.advance(750)
    rig.send(5)
    rig.advance(499)
    assert rig.controller.state == "paused_water"
    rig.advance(1)
    assert rig.controller.state == "running"
    rig.advance(999)
    assert not ids(rig.controller, "progress:")
    rig.advance(1)
    assert rig.controller.state == "finished"


@pytest.mark.parametrize("break_kind", ["zero", "unknown", "fault", "unstable", "stale"])
def test_invalid_reading_breaks_continuous_recovery_hold(make_rig, break_kind):
    rig = make_rig(delays=(1000,))
    rig.begin()
    rig.send(0)
    rig.send(1)
    rig.advance(1500)
    if break_kind == "zero":
        rig.send(0)
    elif break_kind == "unstable":
        rig.send(1, stable=False)
    elif break_kind == "stale":
        # No tick during the gap: receiving a fresh heartbeat must still notice.
        rig.clock.advance(1001)
    else:
        rig.send(None, status=break_kind)
    rig.send(1)
    rig.advance(1999)
    assert rig.controller.state.startswith("paused_")
    assert not ids(rig.controller, "refill:")
    rig.advance(1)
    assert rig.controller.state == "running"
    assert ids(rig.controller, "refill:") == ["refill:1"]


def test_resume_threshold_uses_settings(make_rig):
    settings = DeviceSettings(interaction=InteractionSettings(resume_level=3))
    rig = make_rig(settings=settings)
    rig.begin()
    rig.send(0)
    rig.send(2)
    rig.advance(10000)
    assert rig.controller.state == "paused_water"
    rig.send(3)
    rig.advance(1999)
    assert rig.controller.state == "paused_water"
    rig.advance(1)
    assert rig.controller.state == "running"


def test_unstable_candidate_freezes_without_inventing_water_or_fault(make_rig):
    rig = make_rig(delays=(1000,))
    rig.begin()
    rig.advance(400)
    rig.send(5, stable=False)
    rig.advance(5000)
    assert rig.controller.state == "running"
    assert ids(rig.controller) == ["visitor:idea"]
    rig.send(4)
    rig.advance(599)
    assert not ids(rig.controller, "progress:")
    rig.advance(1)
    assert rig.controller.state == "finished"


def test_unstable_at_due_boundary_cannot_incidentally_finish(make_rig):
    rig = make_rig(delays=(1000,))
    rig.begin()
    rig.advance(750)
    rig.clock.advance(250)
    rig.send(5, stable=False)
    assert ids(rig.controller) == ["visitor:idea"]
    rig.send(0)
    assert rig.controller.state == "paused_water"
    rig.recover()
    assert rig.controller.state == "finished"
    assert ids(rig.controller, "progress:") == ["progress:step-0"]


def test_stale_tick_freezes_at_sample_expiry_and_hides_last_level(make_rig):
    rig = make_rig(delays=(3000,))
    rig.begin()
    rig.clock.advance(1500)
    rig.controller.tick()
    assert rig.controller.state == "paused_sensor"
    assert rig.controller.waterLevel is None
    assert rig.controller.sensorStatus == "unknown"
    assert not ids(rig.controller, "progress:")
    rig.recover()
    rig.advance(1999)
    assert not ids(rig.controller, "progress:")
    rig.advance(1)
    assert rig.controller.state == "finished"


def test_stale_at_final_deadline_precedes_completion(make_rig):
    rig = make_rig(delays=(1500,))
    rig.begin()
    rig.clock.advance(1500)
    rig.controller.tick()
    assert rig.controller.state == "paused_sensor"
    assert not ids(rig.controller, "progress:")
    assert not ids(rig.controller, "summary:")
    rig.recover()
    rig.advance(499)
    assert rig.controller.state == "running"
    rig.advance(1)
    assert rig.controller.state == "finished"


def test_steady_water_remains_fresh_and_completes_once(make_rig):
    rig = make_rig(delays=(5000, 5000))
    rig.begin()
    rig.advance(10000)
    assert rig.controller.state == "finished"
    assert not ids(rig.controller, "fault:")
    rig.send(0)
    rig.send(None, status="fault")
    rig.controller.submit("Duplicate ENTER")
    rig.controller.start()
    for _ in range(5):
        rig.controller.tick()
    assert rig.controller.state == "finished"
    assert rig.controller.idea == "Fixture idea"
    assert ids(rig.controller, "summary:") == ["summary:heading", "summary:body"]
    assert not ids(rig.controller, "water:")


@pytest.mark.parametrize("phase", ["running", "paused_water", "paused_sensor", "finished"])
def test_reset_clears_pending_session_and_requires_fresh_heartbeat(make_rig, phase):
    rig = make_rig(delays=(1000,))
    rig.begin()
    rig.advance(250)
    old_reading = SensorReading((1, 1, 1, 1, 1), 5, "ok", rig.clock())
    if phase == "paused_water":
        rig.send(0)
    elif phase == "paused_sensor":
        rig.send(None, status="fault")
    elif phase == "finished":
        rig.advance(750)
    rig.clock.advance(1)
    controller = rig.controller
    controller.reset()
    assert controller.state == "start"
    assert controller.idea == ""
    assert controller.validationError == ""
    assert controller.waterLevel is None
    assert controller.sensorStatus == "unknown"
    assert not model_rows(controller)
    controller.receiveReading(old_reading)
    controller.start()
    controller.submit("Next visitor")
    assert controller.state == "paused_sensor"
    assert ids(controller) == ["visitor:idea", "fault:1"]
    rig.recover()
    rig.advance(999)
    assert not ids(controller, "progress:")
    rig.advance(1)
    assert controller.state == "finished"
    assert all("Fixture idea" not in row["text"] for row in model_rows(controller))


def test_out_of_order_reading_cannot_interrupt_newer_accepted_sample(make_rig):
    rig = make_rig()
    rig.begin()
    rig.advance(500)
    rig.controller.receiveReading(SensorReading((0, 0, 0, 0, 0), 0, "ok", 0.1))
    assert rig.controller.waterLevel == 5
    assert rig.controller.state == "running"
    assert not ids(rig.controller, "water:")


@pytest.mark.parametrize("text", ["", "   ", "\r\n\t\u2028"])
def test_empty_input_is_rejected_without_starting(make_rig, text):
    rig = make_rig()
    rig.controller.start()
    rig.controller.submit(text)
    assert rig.controller.state == "input"
    assert rig.controller.validationError == rig.controller.copy["empty_input_error"]
    assert rig.controller.idea == ""
    assert not model_rows(rig.controller)


@pytest.mark.parametrize("character", ["a", "💧", "界"])
def test_input_limit_counts_unicode_codepoints_after_trimming(make_rig, character):
    rig = make_rig(delays=(0,))
    rig.send()
    controller = rig.controller
    controller.start()
    controller.submit(character * 501)
    assert controller.state == "input"
    assert controller.validationError == controller.copy["long_input_error"]
    controller.submit(" \n" + character * 500 + " \r\n")
    assert controller.state == "finished"
    assert controller.idea == character * 500
    assert controller.validationError == ""
    assert model_rows(controller)[0]["text"] == character * 500


def test_normalized_plain_user_text_and_literal_interpolation_roles(make_rig):
    rig = make_rig(delays=(0,))
    rig.begin(" \t<script>{idea} {x.__class__}</script>\r\n\nnext\u2028line \n")
    expected = "<script>{idea} {x.__class__}</script> next line"
    controller = rig.controller
    assert controller.idea == expected
    assert model_rows(controller) == [
        {"id": "visitor:idea", "type": "user", "variant": "body", "text": expected},
        {"id": "progress:step-0", "type": "action", "variant": "running", "text": f"Stage 0: {expected}"},
        {"id": "summary:heading", "type": "output", "variant": "H1", "text": "Fixture result"},
        {"id": "summary:body", "type": "output", "variant": "body", "text": f"Result for {expected}"},
    ]
    assert controller.transcript.roleNames() == {
        int(Qt.ItemDataRole.UserRole) + index + 1: name.encode("ascii")
        for index, name in enumerate(TRANSCRIPT_ROLES)
    }
    assert controller.transcript.rowCount(controller.transcript.index(0, 0)) == 0
    assert controller.transcript.data(QModelIndex()) is None
    assert controller.transcript.data(controller.transcript.index(0, 0), Qt.ItemDataRole.DisplayRole) is None


def test_duplicate_submit_and_invalid_state_actions_do_not_skip_messages(make_rig):
    rig = make_rig()
    controller = rig.controller
    controller.submit("Not input")
    assert controller.state == "start"
    assert not model_rows(controller)
    rig.begin("Original")
    for _ in range(5):
        controller.start()
        controller.submit("Duplicate")
        controller.activity()
    assert controller.idea == "Original"
    assert ids(controller) == ["visitor:idea"]
    rig.advance(4500)
    assert controller.state == "finished"
    assert ids(controller, "progress:") == [f"progress:step-{index}" for index in range(3)]


def test_input_activity_and_exact_inactivity_timeout(make_rig):
    rig = make_rig()
    controller = rig.controller
    controller.start()
    rig.clock.advance(119999)
    controller.tick()
    assert controller.state == "input"
    controller.activity()
    rig.clock.advance(119999)
    controller.tick()
    assert controller.state == "input"
    rig.clock.advance(1)
    controller.tick()
    assert controller.state == "start"
    assert not model_rows(controller)


@pytest.mark.parametrize("action", ["submit", "activity"])
def test_input_action_at_expired_deadline_cannot_resurrect_session(make_rig, action):
    rig = make_rig()
    rig.controller.start()
    rig.clock.advance(120000)
    if action == "submit":
        rig.controller.submit("Too late")
    else:
        rig.controller.activity()
    assert rig.controller.state == "start"
    assert rig.controller.idea == ""


def test_finished_timeout_ignores_activity_and_resets_at_sixty_seconds(make_rig):
    rig = make_rig(delays=(0,))
    rig.begin()
    assert rig.controller.state == "finished"
    rig.clock.advance(59999)
    rig.controller.activity()
    rig.controller.tick()
    assert rig.controller.state == "finished"
    rig.clock.advance(1)
    rig.controller.tick()
    assert rig.controller.state == "start"
    assert rig.controller.idea == ""
    assert not model_rows(rig.controller)


@pytest.mark.parametrize("status,level", [("ok", 0), ("unknown", None), ("fault", None)])
def test_pauses_have_no_visitor_inactivity_timeout(make_rig, status, level):
    rig = make_rig()
    rig.controller.start()
    rig.send(level, status=status)
    rig.controller.submit("Wait indefinitely")
    rig.clock.advance(86400000)
    rig.send(level, status=status)
    assert rig.controller.state.startswith("paused_")
    assert rig.controller.idea == "Wait indefinitely"
    assert not ids(rig.controller, "progress:")


def test_qr_source_remains_available_after_session_reset(make_rig):
    rig = make_rig()
    controller = rig.controller
    controller.setQrSource("image://repository/qr")
    assert controller.qrSource == "image://repository/qr"
    controller.qrSource = "image://repository/updated"
    rig.begin()
    controller.reset()
    assert controller.qrSource == "image://repository/updated"


def test_transcript_is_accessible_as_a_model_from_qml(make_rig):
    rig = make_rig()
    rig.begin()
    engine = QQmlEngine()
    context = QQmlContext(engine.rootContext())
    context.setContextProperty("controller", rig.controller)
    expression = QQmlExpression(
        context, None,
        "controller.transcript !== null && controller.transcript.rowCount() === 1",
    )
    result, undefined = expression.evaluate()
    assert not expression.hasError(), expression.error().toString()
    assert not undefined
    assert result is True


def test_configurable_timeouts_and_zero_hold_use_same_scheduler(make_rig):
    settings = replace(DeviceSettings(), interaction=InteractionSettings(
        input_max_length=10, input_inactivity_ms=100, finished_timeout_ms=200, refill_hold_ms=0,
    ))
    rig = make_rig(delays=(0,), settings=settings)
    rig.controller.start()
    rig.clock.advance(100)
    rig.controller.tick()
    assert rig.controller.state == "start"
    rig.controller.start()
    rig.controller.submit("12345678901")
    assert rig.controller.state == "input"
    rig.controller.submit("Short")
    assert rig.controller.state == "paused_sensor"
    rig.send(1)
    assert rig.controller.state == "finished"
    rig.clock.advance(200)
    rig.controller.tick()
    assert rig.controller.state == "start"


@pytest.mark.parametrize("action", ["tick", "activity", "submit"])
def test_fractional_input_deadline_expires_without_an_extra_tick(make_rig, action):
    settings = replace(DeviceSettings(), interaction=InteractionSettings(input_inactivity_ms=200))
    rig = make_rig(settings=settings)
    rig.clock.advance(100)
    rig.controller.start()
    rig.clock.advance(199.999)
    rig.controller.tick()
    assert rig.controller.state == "input"
    rig.clock.advance(0.001)
    if action == "submit":
        rig.controller.submit("Too late")
    else:
        getattr(rig.controller, action)()
    assert rig.controller.state == "start"
    assert not model_rows(rig.controller)


@pytest.mark.parametrize("offset", [100, 170, 123456700])
def test_fractional_recovery_and_remaining_delay_preserve_every_stage(make_rig, offset):
    settings = replace(DeviceSettings(), interaction=InteractionSettings(
        refill_hold_ms=200, finished_timeout_ms=200,
    ))
    rig = make_rig(delays=(200, 100, 200), settings=settings)
    rig.clock.advance(offset)
    rig.begin()
    rig.advance(70)
    rig.send(0)
    rig.advance(30)
    rig.send(1)
    rig.advance(199.999)
    assert rig.controller.state == "paused_water"
    assert not ids(rig.controller, "progress:")
    rig.advance(0.001)
    assert rig.controller.state == "running"
    assert ids(rig.controller, "refill:") == ["refill:1"]
    rig.advance(129.999)
    assert not ids(rig.controller, "progress:")
    rig.advance(0.001)
    assert ids(rig.controller, "progress:") == ["progress:step-0"]
    rig.advance(99.999)
    assert ids(rig.controller, "progress:") == ["progress:step-0"]
    rig.advance(0.001)
    assert ids(rig.controller, "progress:") == ["progress:step-0", "progress:step-1"]
    rig.advance(199.999)
    assert rig.controller.state == "running"
    assert not ids(rig.controller, "summary:")
    rig.advance(0.001)
    assert rig.controller.state == "finished"
    assert ids(rig.controller, "progress:") == [f"progress:step-{index}" for index in range(3)]
    rig.clock.advance(199.999)
    rig.controller.tick()
    assert rig.controller.state == "finished"
    rig.clock.advance(0.001)
    rig.controller.tick()
    assert rig.controller.state == "start"


def test_fractional_sensor_expiry_is_inclusive_then_freezes_progress(make_rig):
    defaults = DeviceSettings()
    settings = replace(defaults, sensors=replace(defaults.sensors, stale_after_ms=200))
    rig = make_rig(delays=(5000,), settings=settings)
    rig.clock.advance(100)
    rig.begin()
    rig.clock.advance(200)
    rig.controller.tick()
    assert rig.controller.state == "running"
    assert rig.controller.sensorStatus == "ok"
    rig.clock.advance(0.001)
    rig.controller.tick()
    assert rig.controller.state == "paused_sensor"
    assert rig.controller.waterLevel is None
    assert not ids(rig.controller, "progress:")
