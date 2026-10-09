# thirsty — Implementation plan

- Status: native kiosk software implemented; workstation evidence recorded in [docs/validation.md](docs/validation.md). Installation release remains blocked on physical acceptance and owner approval.
- Scope: native Qt interaction, sensors, Raspberry Pi deployment tooling, Bluetooth keyboard and HDMI installation.
- The application is runnable, not a shell or contract stub. No physical Pi was available; software completion is not hardware acceptance.
- Sources: [README.md](README.md), [DESIGN.md](DESIGN.md), [Figma Interface](https://www.figma.com/design/Vly8oZbSYachZu9ecP58h8/thirsty?node-id=0-1).
- Labels: **selected** = agreed direction; **default** = working choice; **verify** = needs physical evidence or owner input.

## 1. Selected architecture

| Layer        | Decision                                                                                                                                       |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Hardware     | Raspberry Pi 3 Model A+, 512 MB RAM; HDMI screen; Bluetooth keyboard; five JO-GL534 switches                                                   |
| OS           | Raspberry Pi OS Lite, 32-bit; use packaged dependencies; record the tested OS image and package versions                                       |
| Runtime      | Python 3; one application process; one Qt event loop                                                                                           |
| Interface    | PySide6 / Qt Quick / QML; custom components; local fonts and assets                                                                            |
| Display      | Prefer Qt EGLFS/KMS fullscreen; verify packaged support in TH-02; fallback: minimal Wayland kiosk session if required, record the chosen route |
| GPIO         | GPIO Zero; digital inputs with pull-downs; select the working packaged pin backend in TH-02                                                    |
| Data         | Local JSON for hardware/settings and scripted content; in-memory visitor session                                                               |
| Lifecycle    | systemd; start on boot, restart on failure; fresh Start screen after process restart or power loss                                             |
| Connectivity | Exhibition interaction works offline; Bluetooth remains enabled; Wi-Fi only needed for maintenance                                             |
| Excluded     | Browser runtime, web server, database, cloud AI, actual code generation, deployment, repository creation                                       |

Data flow: `switches → sensor adapter → controller ↔ QML interface ← Bluetooth keyboard`.

- Controller owns session state, transcript and remaining step time.
- Sensor adapter emits readings; QML displays state and submits actions.
- Use Qt timers and monotonic elapsed time; no blocking waits on the UI thread.
- Transfer any GPIO callback to the Qt thread before changing application state.
- Check sensor validity before appending progress or completion; water/fault interruption wins when events coincide.
- Mock sensor mode for development; live mode never silently falls back to mock readings.

## 2. Shared contracts and file ownership

All paths below are implemented and relative to this directory. The contracts are shared across mock and live modes.

| Path                                                                 | Responsibility / contract                                                                                                  | Owner issue                                                 |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `app/main.py`, `app/contracts.py`, `app/config.py`, `pyproject.toml` | Entry point; shared types; validated settings and script loading                                                           | TH-01; entry point integration later owned by TH-09         |
| `app/sensors.py`                                                     | `SensorReading(raw_bits, level, status, sampled_at)`; `level`: 0–5 or null; `status`: unknown / ok / fault                 | TH-03                                                       |
| `app/controller.py`                                                  | `state`, `waterLevel`, `sensorStatus`, transcript model; `start()`, `submit(text)`, `reset()`; Qt properties/signals/slots | TH-06                                                       |
| `app/ui/Theme.qml`, `app/ui/components/`, `app/assets/`              | DESIGN tokens, message variants, water grid, controls, fonts, avatar                                                       | TH-04                                                       |
| `app/ui/Main.qml`, `app/ui/screens/`                                 | Start, Input, Running; bind to controller contract                                                                         | TH-07                                                       |
| `config/device.json`                                                 | Sensor order/polarity, timing defaults, display settings; TH-01 creates schema, TH-02 records tested hardware values       | TH-01 → TH-02                                               |
| `config/script.json`                                                 | All copy, ordered steps, delays, final summary, repository URL                                                             | TH-05                                                       |
| `deploy/`, `docs/device.md`                                          | Device setup and selected packages, graphics and Bluetooth configuration                                                   | TH-02; separate `deploy/systemd/` owned by TH-08            |
| `docs/operator.md`                                                   | Pairing, calibration, reset, restart, recovery                                                                             | TH-10                                                       |
| `tests/`, `docs/validation.md`                                       | Issue-specific tests; final evidence                                                                                       | Each issue owns its test file; TH-11 owns validation report |

Shared data:

- `raw_bits`: latest five physical 0/1 inputs, ordered bottom → top; null until readable. `level` derives from the stabilized pattern. `sampled_at`: monotonic time of the last successful raw read.
- Emit a reading/heartbeat on every poll, even when unchanged; only changed level/status affects the UI. Stale detection must not treat steady water as a disconnected sensor.
- `wet[i] = (raw_bits[i] == wet_value[i])`; polarity is configurable per switch.
- Transcript row: `id`, `type`, `variant`, `text`; use DESIGN's task/action/error/output variants. Display visitor text as plain text.
- Script step: transcript row plus `delay_ms` before insertion; IDs unique; delays nonnegative.
- Script sections: screen copy, progress steps, water/fault messages, final summary, `repository_url`.
- Completion summary and QR are appended only after all progress steps finish with valid water available.
- Missing/invalid configuration produces a clear operator error; no invented URL or assumed full tank.

## 3. Interaction defaults

| State / event              | Behavior                                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Start                      | Figma `2:7`; ENTER opens Input                                                                               |
| Input                      | Figma `2:16`; focus text field; single-line input; ENTER or submit button starts one session                 |
| Input validation           | Trim whitespace; reject empty input; default limit 500 characters; collapse pasted newlines to spaces        |
| Running                    | Figma `2:31`; append scripted messages; scroll to newest message; water indicator stays fixed                |
| Stable level 0             | Enter `paused_water`; append one refill warning per interruption; freeze current step and remaining delay    |
| Refill                     | Default: level ≥1 with valid readings continuously for 2 seconds; resume automatically at the saved position |
| Unknown / faulty sensing   | Enter `paused_sensor`; freeze progress; show one sensor-status message per incident; keep reading sensors    |
| Sensor recovery            | Valid level ≥1 for 2 seconds resumes; valid level 0 enters `paused_water`                                    |
| Submit while dry / unknown | Open Running in the appropriate paused state; do not emit progress first                                     |
| Finished                   | Summary and repository QR in Running; ENTER or a default 60-second timeout returns to Start                  |
| Abandoned Input            | Default: 120 seconds without input returns to Start; no inactivity reset while Running or paused             |
| Reset / restart            | Clear idea, transcript and timers; reread sensors; return to Start                                           |

- Water/fault pause transitions apply to an unfinished session on Running; Start/Input remain navigable.
- `paused_water`, `paused_sensor` and `finished` use the Running layout, not additional Figma screens.
- After completion, water changes update the indicator without restarting the finished script.
- Require a fresh ENTER press across screen transitions; ignore key-repeat submissions.
- Timing and reset values are configurable working defaults, to tune on the installation.
- Default progress sequence is deterministic; the visitor's idea may appear in copy but does not generate code.
- Repository destination: owner-provided, pre-existing app repository; QR generation is local; phone connectivity is required to open it.

## 4. Sensor assumptions and calibration

| Item                    | Working assumption                                                                                              |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- |
| Sensor type             | Passive two-wire switch; verify before connecting                                                               |
| Wiring per switch       | Pi **3.3 V → switch → GPIO input**, with input pull-down; never 5 V on GPIO                                     |
| Electrical reading      | Closed contact = raw 1; open contact = raw 0; GPIO Zero input uses `pull_up=False`                              |
| Water polarity          | Initially wet = closed = 1; dry = open = 0; invert `wet_value` after physical testing if needed                 |
| Sensor order            | S1 lowest through S5 highest; assign and record five distinct BCM pins and physical header pins in TH-02        |
| Filtering               | Default: sample every 50 ms; publish a changed five-bit pattern after 200 ms unchanged; tune during calibration |
| Initialization / errors | Unknown until a stable reading; GPIO read failure becomes a fault immediately                                   |
| Read timeout            | A reading older than 1 second is unknown; no progress based on stale readings                                   |
| Level meaning           | Level 0 = below S1, operationally empty; level 5 = S5 wet, operationally full; not a volume measurement         |

Normalized patterns, bottom → top:

| Wet pattern              | Level                                                                 |
| ------------------------ | --------------------------------------------------------------------- |
| `00000`                  | 0                                                                     |
| `10000`                  | 1                                                                     |
| `11000`                  | 2                                                                     |
| `11100`                  | 3                                                                     |
| `11110`                  | 4                                                                     |
| `11111`                  | 5                                                                     |
| Any other stable pattern | Fault; level null; never count isolated wet switches as a valid level |

- Use 200 ms filtering for accepted level changes; the 2-second refill hold applies after that.
- A disconnected wire can look dry; stuck switches can produce plausible patterns. Software cannot detect every fault with this circuit.
- TH-10 must record actual wet/dry polarity, mounting height and cable behavior for each switch.
- Reference: [GPIO Zero switch wiring and pull-down inputs](https://gpiozero.readthedocs.io/en/stable/api_input.html#button).

## 5. Implementation issues

### TH-01 — Application foundation and contracts

- Status: DONE (software) | Depends: none | Execution: workstation
- Files: foundation paths in §2; `tests/test_config.py`; shared contract definitions.
- Delivered: runnable native application, validated configuration/defaults, concrete Qt-facing controller, mock/live selection, launch command and dependencies.
- Evidence: included in the 364-test workstation suite; explicit configuration errors and mock operation without GPIO hardware. See [validation](docs/validation.md).

### TH-02 — Pi, HDMI and Bluetooth baseline

- Status: BLOCKED (physical); deployment tooling implemented | Depends: TH-01 | Execution: physical Pi
- Files: `deploy/` excluding `deploy/systemd/`; `docs/device.md`; hardware fields in `config/device.json`.
- Deliver: 32-bit Lite setup, packaged Qt/GPIO dependencies, validated graphics backend, fullscreen HDMI output, keyboard pairing/trust/reconnect, keyboard layout, GPIO permissions and pin map.
- Acceptance pending: application types and renders at 1280 × 720; keyboard works after reboot and sleep/wake; no network needed; screen blanking disabled; record OS/packages and idle/typing memory use on 512 MB. No Pi, HDMI or Bluetooth device acceptance has been performed.
- Gate: verify passive contacts before wiring; record provisional polarity explicitly; unresolved package/graphics/memory problems block device deployment, not mock development.

### TH-03 — Sensor adapter

- Status: DONE (software); physical calibration remains TH-10 | Depends: TH-01 | Execution: workstation
- Files: `app/sensors.py`, `tests/test_sensors.py`.
- Deliver: mock and GPIO adapters implementing §4; configurable polarity/order; timestamps, stabilization, fault reporting and clean shutdown.
- Done: tests cover all 32 normalized patterns, inverted polarity, bounce, startup, read failure and stale data; accepted readings reach the Qt thread without blocking UI.

### TH-04 — Theme, assets and reusable QML components

- Status: DONE (software) | Depends: TH-01 | Execution: workstation
- Files: theme/components/assets paths in §2.
- Deliver: complete token mapping, local JetBrains Mono regular/italic and notices, Figma avatar/icons, six water levels, message variants, keyboard-focusable controls.
- Done: compare component captures with Figma; preserve regular vs italic and 400 weight; no default native-control styling; verify font/asset provenance; retain component defaults separately from screen overrides.
- User-feedback visual direction: use the nine supplied original SVG assets with truthful provenance; animate the running icon's three active perimeter cells clockwise at 100ms intervals. Start H1 uses the action token; Running's transcript starts at the 96px top/left tokens and preserves 96px below its viewport, without moving the fixed water indicator.

### TH-05 — Complete script, copy and repository handoff content

- Status: DONE (software); owner copy review pending | Depends: TH-01 | Execution: workstation + owner review
- Files: `config/script.json`.
- Deliver: final Start/Input copy; complete staged app-development sequence with messages and delays; water/refill/fault copy; final summary; readable repository link.
- Done: no filler text; stable message IDs; summary matches staged steps; one shared sequence with safe idea substitution; complete copy ready for review; pending owner approval/URL recorded in §7 for the release gate.
- User-feedback copy direction: use the submitted idea as the app description, with “Mobile App” as the only generic app name; remove PocketPlan branding and visitor-facing fake/staged disclosure. The first progress output is an app plan, followed by mixed task/action messages. Internal provenance and architecture remain explicitly staged; no real app generation is implied by this presentation change.
- Default: 120 seconds of active progress, excluding pauses; tune to physical drainage in TH-10. Chosen destination is `https://zwei.berlin/app-repo`; redirect publication and app content remain release blockers (`output/app/` is empty).

### TH-06 — Experience controller

- Status: DONE (software) | Depends: TH-01 | Execution: workstation
- Files: `app/controller.py`, `tests/test_controller.py`.
- Delivered: §3 state transitions, Qt transcript model, timers, remaining-delay tracking, reset and inactivity handling, integrated with the complete configured script.
- Done: tests with a fake clock interrupt every script stage, including just before completion; repeated refill cycles never skip/duplicate work; dry/unknown starts stay paused; faults, reset and duplicate ENTER are covered.

### TH-07 — Three Figma screens

- Status: DONE (software) | Depends: TH-01, TH-04 | Execution: workstation
- Files: `app/ui/Main.qml`, `app/ui/screens/`.
- Delivered: Start/Input/Running bound to the real controller; standard key events; anchored water display; auto-scrolling transcript; finished summary and QR placement.
- Done: 1280 × 720 screen captures match scoped DESIGN dimensions; long input/messages remain contained; keyboard focus and validation work; errors and completion reuse Running; no horizontal transcript scrolling.
- Display rule: prefer physical 1280 × 720; otherwise preserve 16:9 with uniform scaling/letterboxing; verify pixel assets and QR on the actual screen in TH-11.

### TH-08 — Boot and process recovery

- Status: BLOCKED (physical); systemd and backend tooling implemented | Depends: TH-01, TH-02 | Execution: physical Pi
- Files: `deploy/systemd/`.
- Deliver: application/display startup for TH-02's selected backend; dedicated non-root user with required device permissions; restart-on-failure; bounded volatile logs; operator stop/restart commands.
- Done: cold boot opens fullscreen; killed process restarts to Start; missing keyboard does not crash/block launch and reconnect restores typing; launch works with Wi-Fi off and Bluetooth on; no desktop dialogs cover the UI.

### TH-09 — Integration and local QR generation

- Status: DONE (software); final native entry-point QR smoke passed | Depends: TH-03, TH-05, TH-06, TH-07 | Execution: workstation; live checks in TH-10/11
- Files: `app/main.py`, `app/handoff.py`, dependency manifest if needed, `tests/test_integration.py`.
- Deliver: wire sensors/controller/UI/config together; generate QR locally from the configured repository URL; include its quiet zone and readable URL; validate complete application settings.
- Done: full journey works offline with mock input; live adapter uses the same contract; QR is created once per URL, not per frame; transcript resets between visitors; no visitor ideas in persistent logs; missing URL is an operator configuration error, never a fabricated handoff.
- Test URLs belong only in labeled fixtures; device checks require TH-02/08 and are recorded in TH-10/11.

### TH-10 — Calibration and operator runbook

- Status: BLOCKED (physical); calibration tooling and operator runbook implemented | Depends: TH-02, TH-03, TH-08, TH-09 | Execution: physical installation
- Files: `docs/operator.md`; tested settings in `config/device.json`; timing changes in `config/script.json` coordinated with TH-05 owner.
- Deliver: measured wet/dry polarity, height/order and wiring table; drainage/refill tuning; Bluetooth re-pairing/reconnect steps; next-visitor reset; service stop/restart; shutdown/update and backup-image procedure.
- Done: fill/drain through all six levels; confirm filtering and resume threshold; operator can recover from a sleeping keyboard, sensor fault and restarted process; record power supply/display power arrangement and physical test evidence.

### TH-11 — Installation acceptance

- Status: BLOCKED (physical/owner); mock acceptance work complete | Depends: TH-09, TH-10; owner-approved copy and published destination | Execution: workstation evidence + physical installation
- Files: `docs/validation.md`; orchestrator updates documentation status.
- Delivered: workstation evidence report with versions, screenshots, 100 accelerated actual-QML/controller/mock sessions and measured workstation RSS; see [docs/validation.md](docs/validation.md).
- Acceptance pending: eight-hour run; three physical drain/refill cycles; no crash, OOM or sustained swapping and assessment of long-run memory; responsive typing and scrolling on Pi; boot/recovery and Bluetooth sleep/reconnect; phone scans final QR from HDMI screen.
- Evidence boundary: 100 accelerated sessions do not establish eight-hour stability or Pi memory fit. RSS rose slightly across samples; neither bounded memory nor absence of leaks is established.
- Release gate: unresolved functional/hardware failures remain open; simulated results never count as physical verification.

## 6. Dispatch rules

| Wave | Assignments                                                                                           |
| ---- | ----------------------------------------------------------------------------------------------------- |
| 1    | TH-01: establish contracts and runnable native application                                            |
| 2    | TH-02, TH-03, TH-04, TH-05, TH-06 can run independently after TH-01; respect available agent capacity |
| 3    | TH-07 after TH-04; TH-08 after TH-02                                                                  |
| 4    | TH-09 integration                                                                                     |
| 5    | TH-10 calibration → TH-11 acceptance                                                                  |

- Give each sub-agent its issue, dependencies, shared contracts and relevant DESIGN sections, trim the context to the relevant information.
- One writer per file; orchestrator owns shared-contract changes and this backlog.
- Status values: TODO / IN_PROGRESS / BLOCKED / DONE; record blocker or completion evidence beside status.
- Handoff: files changed, checks run, hardware actually tested, remaining blocker.
- If hardware is unavailable, mark only physical work blocked and continue independent mock work.

Technical references: [Pi 3 A+ specifications](https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-a-plus-product-brief.pdf), [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/), [Qt embedded display backends](https://doc.qt.io/qt-6.8/embedded-linux.html), [PySide6 Qt Quick package](https://packages.debian.org/trixie/python3-pyside6.qtquick).

## 7. Approval and installation release checklist

Software work proceeds without further user confirmation. The following are explicit release gates, not reasons to leave independent software unfinished:

- [x] Native application, complete script, theme/assets, controller, sensor adapters and deployment/calibration tooling implemented.
- [x] Workstation suite: 364 tests; 98 runtime Theme values match DESIGN; 28 source events and 43 provenance quotes checked. Five deployment-review defects corrected with portable regression coverage, not Pi acceptance.
- [x] Native pause/refill/finish/reset/scaling captures and real QTimer refill-hold smoke; 100 accelerated actual-QML/controller/mock sessions.
- [x] Final integrated native entry-point smoke: real timers/mock-file sensing, all 18 stages, rendered QR independently decoded to the chosen URL; reset and clean exit.
- [ ] Owner reviews and approves complete visitor-facing copy.
- [ ] Publish the chosen `https://zwei.berlin/app-repo` redirect and its intended pre-existing app destination; `output/app/` currently contains no app.
- [ ] Confirm passive switch contacts before wiring; measure polarity/order and approve final pin map. Provisional/unverified pins must not be represented as tested.
- [ ] Complete TH-02 hardware baseline and TH-08 cold-boot/restart/offline/Bluetooth acceptance on the actual Pi.
- [ ] Complete TH-10 physical calibration, drainage timing and operator recovery.
- [ ] Complete TH-11 eight-hour soak, Pi memory assessment, three physical drain/refill cycles and phone scan from installed HDMI display.

See [operator procedures](docs/operator.md), [device setup](docs/device.md) and [validation evidence](docs/validation.md). No physical installation checks have been performed.
