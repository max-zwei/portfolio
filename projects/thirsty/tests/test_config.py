"""Configuration-only tests. URLs here are explicitly labeled test fixtures.

The fixture builder can also supply a shell smoke script to the orchestrator;
it is never loaded implicitly by the production application.
"""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import json

import pytest

from app.config import (
    ConfigurationError,
    DeviceSettings,
    DisplaySettings,
    InteractionSettings,
    SensorSettings,
    load_device,
    load_script,
    parse_device,
    parse_script,
)
from app.contracts import SensorReading, TRANSCRIPT_ROLES


def script_fixture() -> dict:
    """TEST FIXTURE ONLY: example.org is not a production handoff destination."""
    return {
        "copy": {
            "start_title": "TEST FIXTURE — thirsty",
            "start_body": "TEST FIXTURE ONLY — synthetic introduction body.",
            "start_prompt": "Press ENTER to begin",
            "input_title": "Describe an app",
            "input_prompt": "What would you like to make?",
            "input_placeholder": "Your app idea",
            "input_submit_label": "Submit app idea",
            "empty_input_error": "Please enter an app idea.",
            "long_input_error": "Please shorten your app idea.",
            "running_title": "Working on your app",
            "finished_prompt": "Press ENTER for the next visitor",
            "repository_label": "App repository",
            "water_label": "Water level",
            "sensor_unknown_label": "Waiting for water sensors",
            "sensor_fault_label": "Water sensing needs attention",
        },
        "progress": [
            {"id": "plan", "type": "task", "variant": "H1", "text": "Planning {idea}", "delay_ms": 0},
            {"id": "backend", "type": "action", "variant": "running", "text": "Working on the backend", "delay_ms": 12000},
        ],
        "water": {"id": "water-pause", "type": "error", "variant": "water_level", "text": "Please refill the water."},
        "refill": {"id": "water-resume", "type": "action", "variant": "running", "text": "Water restored. Continuing."},
        "fault": {"id": "sensor-pause", "type": "action", "variant": "error", "text": "Waiting for reliable water sensors."},
        "final_summary": [
            {"id": "summary", "type": "output", "variant": "body", "text": "The staged planning and backend work is complete."}
        ],
        "repository_url": "https://example.org/thirsty-test-fixture",
    }


def test_documented_defaults_and_immutable_settings():
    settings = parse_device({})
    assert settings.sensors.pins == (None,) * 5
    assert settings.sensors.physical_pins == (None,) * 5
    assert settings.sensors.wet_values == (1,) * 5
    assert settings.sensors.poll_interval_ms == 50
    assert settings.sensors.stable_for_ms == 200
    assert settings.sensors.stale_after_ms == 1000
    assert settings.interaction.refill_hold_ms == 2000
    assert settings.interaction.input_max_length == 500
    assert settings.interaction.input_inactivity_ms == 120000
    assert settings.interaction.finished_timeout_ms == 60000
    assert settings.interaction.resume_level == 1
    assert (settings.display.width, settings.display.height) == (1280, 720)
    with pytest.raises(FrozenInstanceError):
        settings.sensors.poll_interval_ms = 100


def test_unverified_pin_map_allows_mock_but_never_live():
    settings = DeviceSettings()
    settings.validate_for_mode("mock")
    with pytest.raises(ConfigurationError, match="five configured, distinct BCM pins"):
        settings.validate_for_mode("live")
    configured = parse_device({"sensors": {"pins": [2, 3, 4, 17, 27]}})
    configured.validate_for_mode("live")
    with pytest.raises(ConfigurationError, match="mode"):
        configured.validate_for_mode("automatic")


def test_pin_order_is_preserved_not_sorted_and_polarity_need_not_be_contiguous():
    settings = parse_device({"sensors": {"pins": [27, 2, 17, 4, 3], "wet_values": [0, 1, 0, 1, 0]}})
    assert settings.sensors.pins == (27, 2, 17, 4, 3)
    assert settings.sensors.wet_values == (0, 1, 0, 1, 0)


@pytest.mark.parametrize("section,field,value", [
    ("sensors", "pins", [1, 2, 3, 4]),
    ("sensors", "pins", [1, 2, 3, 4, 4]),
    ("sensors", "pins", [-1, 2, 3, 4, 5]),
    ("sensors", "pins", [28, 2, 3, 4, 5]),
    ("sensors", "pins", [True, 2, 3, 4, 5]),
    ("sensors", "physical_pins", [0, None, None, None, None]),
    ("sensors", "physical_pins", [41, None, None, None, None]),
    ("sensors", "physical_pins", [3, 3, None, None, None]),
    ("sensors", "wet_values", [1, 1, 1, 1, 2]),
    ("sensors", "wet_values", [True, 1, 1, 1, 1]),
    ("sensors", "wet_values", "11111"),
    ("sensors", "poll_interval_ms", 0),
    ("sensors", "poll_interval_ms", 60001),
    ("sensors", "poll_interval_ms", 50.0),
    ("sensors", "stable_for_ms", -1),
    ("sensors", "stable_for_ms", 60001),
    ("sensors", "stale_after_ms", 49),
    ("sensors", "stale_after_ms", 3600001),
    ("sensors", "pin_factory", "mock"),
    ("sensors", "pin_factory", 1),
    ("sensors", "hardware_verified", "false"),
    ("interaction", "input_max_length", 0),
    ("interaction", "input_max_length", 10001),
    ("interaction", "input_max_length", True),
    ("interaction", "input_inactivity_ms", 0),
    ("interaction", "input_inactivity_ms", 86400001),
    ("interaction", "finished_timeout_ms", -1),
    ("interaction", "finished_timeout_ms", 86400001),
    ("interaction", "refill_hold_ms", -1),
    ("interaction", "refill_hold_ms", 86400001),
    ("interaction", "resume_level", 0),
    ("interaction", "resume_level", 6),
    ("display", "width", 319),
    ("display", "width", 7681),
    ("display", "height", 179),
    ("display", "height", 4321),
    ("display", "fullscreen", 1),
])
def test_reject_invalid_device_field(section, field, value):
    with pytest.raises(ConfigurationError, match=field):
        parse_device({section: {field: value}})


def test_inclusive_configuration_bounds():
    assert SensorSettings(poll_interval_ms=1, stable_for_ms=0, stale_after_ms=1).stable_for_ms == 0
    assert SensorSettings(poll_interval_ms=60000, stable_for_ms=60000, stale_after_ms=3600000).poll_interval_ms == 60000
    assert InteractionSettings(input_max_length=1, refill_hold_ms=0, resume_level=5).refill_hold_ms == 0
    assert InteractionSettings(input_max_length=10000, input_inactivity_ms=86400000, finished_timeout_ms=86400000, refill_hold_ms=86400000).input_max_length == 10000
    assert DisplaySettings(width=320, height=180).width == 320
    assert DisplaySettings(width=7680, height=4320).height == 4320


@pytest.mark.parametrize("value", [[], None, "device", {"sensor": {}}, {"sensors": {"poll_ms": 50}}, {"display": None}])
def test_device_rejects_wrong_shapes_and_unknown_fields(value):
    with pytest.raises(ConfigurationError):
        parse_device(value)


def test_complete_script_contract_and_stable_ids():
    script = parse_script(script_fixture())
    assert script.progress[0].text == "Planning {idea}"
    assert script.progress[0].delay_ms == 0
    assert script.copy.as_qml()["input_submit_label"] == "Submit app idea"
    assert script.final_summary[0].type == "output"
    assert [row.id for row in script.progress] == ["plan", "backend"]
    assert TRANSCRIPT_ROLES == ("id", "type", "variant", "text")
    assert isinstance(script.progress, tuple)
    assert isinstance(script.final_summary, tuple)


@pytest.mark.parametrize("url", [None, "", "  ", 42, "repository", "/repo", "ftp://example.org/repo", "https:///repo", "https://user:pass@example.org/repo", "https://example.org:99999/repo", "https://example.org:0/repo", " https://example.org/repo", "https://example.org/a b", "https://example.org/\nrepo", "https://example.org\\repo"])
def test_invalid_repository_urls_are_explicit_operator_errors(url):
    value = script_fixture()
    value["repository_url"] = url
    with pytest.raises(ConfigurationError, match="repository_url"):
        parse_script(value)


def test_absent_repository_url_has_actionable_error():
    value = script_fixture()
    del value["repository_url"]
    with pytest.raises(ConfigurationError, match="owner-provided app repository URL is required"):
        parse_script(value)


@pytest.mark.parametrize("url", ["https://example.org/repo", "http://localhost:8080/repo", "https://example.org/repo?view=code#readme"])
def test_absolute_http_repository_urls_are_accepted(url):
    value = script_fixture()
    value["repository_url"] = url
    assert parse_script(value).repository_url == url


@pytest.mark.parametrize("field,value", [
    ("id", ""), ("id", "1start"), ("id", "space id"), ("id", "reserved:prefix"),
    ("type", "assistant"), ("type", "user"), ("type", True), ("type", []),
    ("variant", "h1"), ("variant", "water_level"), ("variant", False),
    ("text", ""), ("text", None), ("text", "{idea.__class__}"),
    ("text", "{idea!r}"), ("text", "{idea:>100}"), ("text", "{unknown}"),
    ("text", "unclosed {idea"),
    ("delay_ms", -1), ("delay_ms", True), ("delay_ms", 0.5), ("delay_ms", 3600001),
])
def test_progress_schema_rejects_invalid_values(field, value):
    script = script_fixture()
    script["progress"][0][field] = value
    with pytest.raises(ConfigurationError, match=field):
        parse_script(script)


def test_step_delays_accept_upper_bound():
    script = script_fixture()
    script["progress"][0]["delay_ms"] = 3600000
    assert parse_script(script).progress[0].delay_ms == 3600000


@pytest.mark.parametrize("section", ["progress", "final_summary"])
@pytest.mark.parametrize("value", [[], {}, None])
def test_script_requires_nonempty_ordered_message_arrays(section, value):
    script = script_fixture()
    script[section] = value
    with pytest.raises(ConfigurationError, match=section):
        parse_script(script)


@pytest.mark.parametrize("section", ["water", "refill", "fault", "final_summary"])
def test_duplicate_ids_rejected_across_all_sections(section):
    script = script_fixture()
    target = script[section][0] if section == "final_summary" else script[section]
    target["id"] = script["progress"][0]["id"]
    with pytest.raises(ConfigurationError, match="duplicate message ID"):
        parse_script(script)


@pytest.mark.parametrize("section,type_,variant", [
    ("water", "action", "error"),
    ("refill", "task", "body"),
    ("fault", "output", "body"),
    ("final_summary", "task", "body"),
])
def test_incident_and_summary_sections_use_required_design_variants(section, type_, variant):
    script = script_fixture()
    target = script[section][0] if section == "final_summary" else script[section]
    target.update(type=type_, variant=variant)
    with pytest.raises(ConfigurationError, match=section):
        parse_script(script)


def test_unknown_copy_fields_missing_copy_and_extra_step_fields_are_rejected():
    base = script_fixture()
    bad = deepcopy(base)
    bad["copy"]["heading"] = "unknown"
    with pytest.raises(ConfigurationError, match="heading"):
        parse_script(bad)
    for field in ("start_prompt", "start_body"):
        bad = deepcopy(base)
        del bad["copy"][field]
        with pytest.raises(ConfigurationError, match=rf"copy: missing required field\(s\): {field}"):
            parse_script(bad)
    bad = deepcopy(base)
    bad["progress"][0]["delay"] = 1
    with pytest.raises(ConfigurationError, match="delay"):
        parse_script(bad)
    bad = deepcopy(base)
    bad["final_summary"][0]["delay_ms"] = 0
    with pytest.raises(ConfigurationError, match="delay_ms"):
        parse_script(bad)


@pytest.mark.parametrize("body", [None, "", " \n\t", 42])
def test_start_body_requires_nonblank_text(body):
    script = script_fixture()
    script["copy"]["start_body"] = body
    with pytest.raises(ConfigurationError, match=r"copy\.start_body"):
        parse_script(script)


def test_loaders_preserve_source_path_and_reject_duplicate_json_keys(tmp_path):
    missing = tmp_path / "missing.json"
    with pytest.raises(ConfigurationError, match="missing.json"):
        load_device(missing)
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"display": {}, "display": {}}', encoding="utf-8")
    with pytest.raises(ConfigurationError, match="invalid.json.*duplicate"):
        load_device(invalid)
    invalid.write_text('{"sensors": {"poll_interval_ms": NaN}}', encoding="utf-8")
    with pytest.raises(ConfigurationError, match="non-finite"):
        load_device(invalid)
    invalid.write_text("{", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="invalid.json"):
        load_device(invalid)
    invalid.write_bytes(b"\xff")
    with pytest.raises(ConfigurationError, match="invalid.json"):
        load_device(invalid)


def test_valid_json_files_load_as_typed_settings_and_script(tmp_path):
    device_path = tmp_path / "device.json"
    device_path.write_text("{}", encoding="utf-8")
    assert load_device(device_path) == DeviceSettings()
    script_path = tmp_path / "explicitly-labeled-test-fixture.json"
    script_path.write_text(json.dumps(script_fixture()), encoding="utf-8")
    assert load_script(script_path).repository_url == script_fixture()["repository_url"]


def test_direct_dataclass_construction_cannot_bypass_validation():
    with pytest.raises(ConfigurationError, match="sensors"):
        DeviceSettings(sensors={})
    script = parse_script(script_fixture())
    with pytest.raises(ConfigurationError, match="repository_url"):
        replace(script, repository_url="")
    with pytest.raises(ConfigurationError, match="delay_ms"):
        replace(script, progress=(replace(script.progress[0], delay_ms=-1),))


def test_reading_distinguishes_latest_raw_from_stabilized_level():
    reading = SensorReading((1, 0, 0, 0, 0), 5, "ok", 10.0, is_stable=False)
    assert reading.level == 5
    assert reading.raw_bits == (1, 0, 0, 0, 0)
    assert reading.sampled_at == 10.0
    assert not reading.is_stable
    fault = SensorReading((1, 0, 1, 0, 0), None, "fault", 10.0)
    assert fault.level is None  # Noncontiguous raw input is representable, never counted here.
    assert SensorReading(None, None, "unknown", None).sampled_at is None


@pytest.mark.parametrize("kwargs", [
    {"raw_bits": [1, 1, 1, 1, 1]},
    {"raw_bits": (True, 1, 1, 1, 1)},
    {"raw_bits": (1, 0)},
    {"raw_bits": (2, 0, 0, 0, 0)},
    {"level": 6}, {"level": True}, {"level": None},
    {"status": "full"}, {"status": "fault"},
    {"sampled_at": None}, {"sampled_at": -1}, {"sampled_at": float("nan")},
    {"is_stable": 1},
])
def test_sensor_reading_contract_rejects_invalid_fields(kwargs):
    values = dict(raw_bits=(1, 1, 1, 1, 1), level=5, status="ok", sampled_at=10.0)
    values.update(kwargs)
    with pytest.raises(ValueError):
        SensorReading(**values)
