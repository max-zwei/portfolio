# Operator runbook and calibration — TH-10

## Status, authority and installation limits

**Physical commissioning is BLOCKED: no Raspberry Pi, switches, tank, display or keyboard has been available for measurement.** This is an actionable procedure, not a completed calibration or a claim of hardware acceptance. No checks or experiments were run while writing it. Complete the dated, private installation record before admitting visitors; a software test or successful inventory cannot stand in for physical evidence.

Read [device setup](device.md) for the package/electrical baseline, [boot lifecycle](../deploy/systemd/README.md) for the actual service/approval contract, [PRODUCT §4](../PRODUCT.md#4-sensor-assumptions-and-calibration) for sensing semantics and [copy review](copy-review.md) for content provenance. Commands below are for an authorized maintenance operator on the selected Pi unless explicitly labelled otherwise. Run project-relative commands from the reviewed checkout installed at `/opt/thirsty`. The public application command is `/usr/bin/python3 -m app`; backend selection belongs to deployment tooling, not an application flag.

The artwork replays the existing recorded PocketPlan sequence. It does not create the visitor's requested app, run an AI service, build software, deploy a site or create a repository. **Do not run or modify `experiment/` or its capture scripts. Keep `output/app/` completely empty**, including no `.gitkeep`, generated QR, copied recording, sample app or backup. Store installation evidence and backups outside that directory and outside visitor-accessible storage.

### Explicit unmeasured / blocked installation record

Fill a private record with date, operator, instrument/tool, observed value, pass/fail and evidence reference for each row. Never replace “unmeasured” with a default, manufacturer rating or inventory flag. Do not commit passwords, Bluetooth addresses, Wi-Fi credentials or visitor text.

| Required evidence                                                                                                        | Current status / release consequence                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Actual board model, RAM, userspace and interpreter architecture                                                          | **Unmeasured / blocked.** Required: Raspberry Pi 3 Model A+, 512 MB, Raspberry Pi OS Lite Trixie, 32-bit armhf userspace and interpreter. A 64-bit kernel alone does not disqualify or prove this. |
| Exact official image filename, release, URL, published/calculated SHA-256, flash verification, card and project revision | **Unrecorded / blocked.** Follow `device.md`; never substitute another image's checksum.                                                                                                           |
| Installed package versions, graphics plugin availability and non-root permissions                                        | **Untested / blocked.** Attach target preflight evidence; packaged availability is not a render test.                                                                                              |
| Chosen EGLFS/KMS or Weston/Wayland route, DRM card/connector, active VT/seat, GPU renderer and actual 1280 × 720 output  | **Unverified / blocked.** Neither route is approved.                                                                                                                                               |
| Display model, power arrangement, blanking and monitor sleep                                                             | **Unmeasured / blocked.** Record how both Pi and screen receive power and the idle trial duration.                                                                                                 |
| Pi supply, cable, loaded voltage/power behavior, temperature and throttling                                              | **Unmeasured / blocked.** 5 V / 2.5 A is the Pi supply specification, not a measured result and never a GPIO voltage.                                                                              |
| All five passive contacts, isolation, rail voltage, BCM/header map, wet/dry polarity, heights and cable behavior         | **Unmeasured / blocked.** See the five-switch record below.                                                                                                                                        |
| Drainage time, refill quantity/height, bounce/filter response and resume hold                                            | **Unmeasured / blocked.** JSON timing values are working defaults only.                                                                                                                            |
| Bluetooth pairing, layout, sleep/wake, power-cycle and absent-at-boot recovery                                           | **Untested / blocked.** Keep a wired/local recovery console.                                                                                                                                       |
| Offline cold boot, service recovery, GPIO cleanup and safe shutdown                                                      | **Untested / blocked.** Wi-Fi off must not turn Bluetooth off.                                                                                                                                     |
| Idle/typing/scrolling memory, swap, eight-hour run and three physical drain/refill cycles                                | **Unmeasured / blocked.** 512 MB acceptance requires actual observations; do not call a workstation run a Pi pass.                                                                                 |
| Final owner copy approval                                                                                                | **Pending / blocked for release.** Record approval of the installed `config/script.json` revision.                                                                                                 |
| `https://zwei.berlin/app-repo` redirect, intended existing repository and phone QR scan from HDMI                        | **Owner redirect pending; destination and scan unverified / blocked for release.** Local QR rendering does not establish any of these.                                                             |
| Recoverable full-card backup and spare-card restore trial                                                                | **Not performed / blocked for unattended operation.** Record image hash and restore result privately.                                                                                              |

Repository `config/device.json` intentionally has five null `sensors.pins`, five null `physical_pins`, `pin_factory: null` and `hardware_verified: false`. Keep unresolved values that way. Its five `wet_values: 1` entries are provisional, not measurements. Do not set approval flags simply to make a refused launch proceed.

## 1. Prepare the target and approve the display

1. Use the specified Pi 3 A+ / 512 MB and a verified official **Trixie Lite 32-bit** image. Install the reviewed project, local fonts/assets and JSON under `/opt/thirsty`, root-owned, without group/world write access or symlinks. Do not copy a workstation virtual environment. Preserve a separate maintenance console, normally VT1, and a recovery keyboard; VT7 belongs exclusively to the kiosk.
2. Follow the complete signed-package procedure in `device.md`. For the explicitly selected package-supported Wayland candidate, the exact commands are:

   ```sh
   sudo apt-get update
   bash deploy/setup-device.sh --display-backend wayland
   sudo bash deploy/setup-device.sh --display-backend wayland --apply
   /usr/bin/python3 deploy/preflight.py --display-backend wayland --require-pi --require-software --output /tmp/thirsty-preflight.json
   ```

   Review the simulated plan before `--apply`; apt asks for confirmation. Choose a new output filename for every preflight: it refuses overwrites. Run preflight as a non-root user and again as the final kiosk identity/session. Archive the reviewed report privately before shutdown; `/tmp` and the kiosk journal are not evidence archives. A wrong board/architecture, missing package/plugin, OOM or sustained swapping blocks deployment; do not solve it with arbitrary repositories, pip Qt wheels or a software-renderer fallback.

3. Trial the chosen display with **explicit mock sensors**, following `device.md`, on the actual screen and an active local non-root VT. EGLFS is conditional on the installed official build providing both EGLFS and KMS integration plugins; the documented stock Trixie packages do not establish that route. Wayland must be explicitly chosen and installed, not used as an automatic fallback. Do not run both display owners, use root Qt/Weston, grant `chmod 666` device access or enable a competing getty on VT7.
4. Observe the actual DRM card, backend-reported connector, active seat, keyboard layout, GPU renderer and physical scanout. Prove 1280 × 720, local font/SVG/QR rendering, responsive synthetic typing, prolonged idle without blanking and the monitor's own sleep policy. App width/height are not proof of HDMI mode. Record any physical 16:9 scaling/letterboxing exception; do not invent a connector or accept llvmpipe just because an image appears.
5. Prepare the private approval JSON required by `deploy/systemd/install.py`: `backend`, `drm_card`, `connector`, `keyboard_layout`, `record`, and `graphics_verified`, `seat_verified`, `permissions_verified`, `blanking_verified`. The four booleans become true **only after the corresponding physical trials**. Follow the exact EGLFS JSON or Weston INI format in the lifecycle document. Example source locations below are `/root/thirsty-maintenance/approval.json` and `/root/thirsty-maintenance/weston.ini`; these are operator-created files, not supplied approvals.
6. After display approval, install a mock-mode service trial explicitly:

   ```sh
   sudo /usr/bin/python3 deploy/systemd/install.py --display-backend wayland --mode mock \
     --approval /root/thirsty-maintenance/approval.json \
     --display-config /root/thirsty-maintenance/weston.ini --apply
   sudo systemctl start thirsty.service
   systemctl status thirsty.service
   journalctl --namespace=thirsty -u thirsty.service --since today
   loginctl session-status
   sudo systemctl stop thirsty.service
   ```

   The installer never starts the service; applying without `--enable` leaves it disabled, including a previously enabled installation. It validates but cannot physically prove the operator assertions. Do not enable exhibition boot while still in mock mode. For a physically approved EGLFS route, select `--display-backend eglfs` and its approved `eglfs.json` instead; repeat the full installer selection, never change only an environment variable.

## 2. Electrical and water safety — before connecting GPIO

Only a competent installer may commission the circuit. Remove visitors, close/control the drain and use a stable catch container. Keep the Pi, microSD, power supplies, mains connections, exposed connectors and display electronics outside the fill, splash, overflow and drainage paths. Provide strain relief, protected dry connections and drip loops; secure cables so a visitor cannot pull them into water. Record the actual enclosure and supply/display power arrangement. Neither software nor a sensor contact rating certifies electrical or water safety.

1. **Power down and disconnect every supply before wiring or continuity tests**, including possible power from attached peripherals. Separate the five sensors from the Pi and all supplies. Never use a meter's resistance/continuity range on a powered circuit.
2. Label switches and both ends of their cables **S1 lowest through S5 highest**. With each sensor electrically isolated, confirm it is a passive, isolated two-wire contact rather than a powered module or active voltage output. Measure dry and immersed continuity in its installed orientation; repeat rising/falling water to find actuation/release heights and hysteresis. Record meter readings, not just “seems to switch.” Check for unexpected conduction to the water, enclosure and other conductors using appropriate equipment and the manufacturer's constraints. An ambiguous result blocks connection.
3. Choose five distinct BCM input numbers after checking enabled interfaces and actual wiring. Use the [official Raspberry Pi GPIO/header reference](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio), board pin-1 orientation and `deploy/systemd/gate.py`'s BCM/header correspondence. `pins` means **BCM**, not the physical connector position; `physical_pins` records the corresponding **1–40 header position**. Avoid pins reserved by enabled I²C/SPI/UART or other installation hardware. A valid numeric mapping does not prove a pin is free.
4. Wire only the verified topology: **Pi 3.3 V → passive contact → selected GPIO input**, with GPIO Zero `pull_up=False`. The header's physical **1/17 are 3.3 V; 2/4 are 5 V**; this distinction is a safety reference, not an assignment of sensor inputs. Never connect a GPIO to 5 V, to a sensor's maximum rated voltage, or to an external powered output. Do not use random jumpers, `gpioset`, output-driving probes or short GPIO to a rail to simulate water.
5. Before connecting the sensor harness to any input, a qualified installer must verify the source and every harness path with suitable measurements: actual rail referenced to Pi ground, correct ground identification, no continuity to the 5 V rail with supplies disconnected, and **no 5 V/external voltage on any line intended for GPIO**. Powered voltage measurement, if required, is a controlled dry-bench operation with the harness isolated from GPIO; use probes/fixtures that cannot bridge adjacent header pins. De-energize again before attaching or changing the harness. A rail label is not this verification. Record measured voltages and instrument, leaving them unmeasured until performed.
6. Inspect correct pin orientation, insulated terminations, pull-down design, cable isolation and tank/electronics separation. For each lead, gently flex the intended installed cable route during isolated wet/dry tests; note intermittency, false transitions, contact bounce and strain. Repair hardware faults rather than hiding them with a longer filter.

### Five-switch calibration record — no assignments or measurements supplied

Measure heights in millimetres from one recorded fixed tank datum, at the installed orientation. Record both rising-water actuation and falling-water release, not an assumed uniform spacing. Use private evidence references for detailed continuity/voltage readings and cable results.

| Switch / array index | Physical order | BCM `pins`        | Header `physical_pins` | Dry contact / raw bit | Wet contact / raw bit | `wet_values`  | Actuation / release height | Cable behavior / evidence |
| -------------------- | -------------- | ----------------- | ---------------------- | --------------------- | --------------------- | ------------- | -------------------------- | ------------------------- |
| S1 / 0               | Lowest         | null — unverified | null — unverified      | Unmeasured            | Unmeasured            | 1 provisional | Unmeasured                 | Untested / blocked        |
| S2 / 1               | Second         | null — unverified | null — unverified      | Unmeasured            | Unmeasured            | 1 provisional | Unmeasured                 | Untested / blocked        |
| S3 / 2               | Middle         | null — unverified | null — unverified      | Unmeasured            | Unmeasured            | 1 provisional | Unmeasured                 | Untested / blocked        |
| S4 / 3               | Fourth         | null — unverified | null — unverified      | Unmeasured            | Unmeasured            | 1 provisional | Unmeasured                 | Untested / blocked        |
| S5 / 4               | Highest        | null — unverified | null — unverified      | Unmeasured            | Unmeasured            | 1 provisional | Unmeasured                 | Untested / blocked        |

In the specified circuit, closed is electrically raw 1 and open raw 0. **Wet is not necessarily closed.** Set each `wet_values[i]` to that switch's actually observed wet raw value. If wet opens the contact, use 0 for that entry; confirm its dry raw value is 1. Reordering a cable requires rechecking all corresponding array entries, not just swapping one polarity. Operational level is not a volume measurement: level 0 is below S1 and may leave residual water; level 5 means S5 wet, not permission to fill above a safe maximum.

## 3. Supervised input commissioning and configuration

Do not run the service and a GPIO diagnostic concurrently. After the entire electrical gate passes, enter the measured BCM/header assignments and polarity in the **device's** `config/device.json`; retain `hardware_verified: false` until backend/input verification is complete. Do not invent values or change the repository's unresolved installation record without evidence. The candidate backend is packaged `lgpio`, not an automatic alternative or a remote pigpio daemon.

A qualified operator can use this bounded **input-only** diagnostic after authorizing the mapped circuit. It is not a deployment or safety bypass: it intentionally does not start the app, and must not be run against unknown wiring. Stop `thirsty.service` first. Run from `/opt/thirsty` as a non-root maintenance identity whose actual GPIO-chip access has been approved. Do not use root to hide a permission error. Mock service installation omits the kiosk user's `gpio` group; the physical commissioning operator must resolve approved access before attempting GPIO, not relax device-node permissions.

The diagnostic creates a private temporary `LG_WD` before importing GPIO Zero/lgpio. Packaged lgpio 0.2.2 creates notification files during import; the root-owned `/opt/thirsty` checkout is not a writable working directory. Cleanup closes every opened input and the factory before removing this diagnostic's temporary directory, including on an ordinary exception or Ctrl+C. It stores no visitor data and never removes another process's GPIO resources.

```sh
sudo systemctl stop thirsty.service
/usr/bin/python3 - <<'PY'
import os
import tempfile
import time
from contextlib import ExitStack

with tempfile.TemporaryDirectory(prefix='thirsty-gpio-') as gpio_workdir, ExitStack() as cleanup:
    os.environ['LG_WD'] = gpio_workdir
    from app.config import load_device

    sensors = load_device('config/device.json').sensors
    if any(pin is None for pin in sensors.pins + sensors.physical_pins):
        raise SystemExit('Stop: complete and independently verify the BCM/header record first')
    from gpiozero import DigitalInputDevice
    from gpiozero.pins.lgpio import LGPIOFactory

    factory = LGPIOFactory()
    cleanup.callback(factory.close)
    inputs = []
    for pin in sensors.pins:
        sensor = DigitalInputDevice(pin, pull_up=False, pin_factory=factory)
        cleanup.callback(sensor.close)
        inputs.append(sensor)
    deadline = time.monotonic() + 30
    previous = None
    while time.monotonic() < deadline:
        raw = tuple(int(sensor.value) for sensor in inputs)
        if raw != previous:
            wet = tuple(int(bit == polarity) for bit, polarity in zip(raw, sensors.wet_values))
            print(f'{time.monotonic():.3f} raw={raw} normalized_wet={wet}', flush=True)
            previous = raw
        time.sleep(sensors.poll_interval_ms / 1000)
PY
```

During each bounded run, deliberately change only identified switch states by safe water movement or manufacturer-permitted mechanical actuation, never by live rewiring. Record the actual dry/wet raw bits and verify S1–S5 identity at the installed cable lengths. Repeat as needed to cover all switches. The printed data is **unfiltered** and timestamps are monotonic, not a calibrated latency measurement; transitions faster than polling require suitable measurement equipment. GPIO errors, inconsistent polarity or intermittent cables block live approval. Close the diagnostic before starting the application.

After electrical safety, mapping, polarity and actual lgpio input access are evidenced, set `sensors.pin_factory` to `"lgpio"` and `hardware_verified` to true on the commissioned device. That flag is the operator's assertion, not software certification and not completion of the six-level/timing trials below. If wiring, switch type, orientation or backend changes, stop live use, revoke the assertion and repeat the affected measurements. Physical acceptance remains open until the live service works under the final non-root `thirsty` identity and every trial passes.

With approved display files and sensors, install **live without boot enablement**, then start the supervised trial:

```sh
sudo /usr/bin/python3 deploy/systemd/install.py --display-backend wayland --mode live \
  --approval /root/thirsty-maintenance/approval.json \
  --display-config /root/thirsty-maintenance/weston.ini --apply
sudo systemctl start thirsty.service
systemctl status thirsty.service
journalctl --namespace=thirsty -u thirsty.service --since today
```

Use the already approved EGLFS selection instead only if that is the installation's recorded route. Do not launch a second app manually while the service owns the seat. The integrated live application command used by the service is:

```sh
/usr/bin/python3 -m app --mode live --device /opt/thirsty/config/device.json \
  --script /opt/thirsty/config/script.json --fullscreen
```

That command alone does not create an active seat, select Qt's backend or prepare a compositor; use the lifecycle tools. A live error must stay visible to the operator and never silently become mock water.

## 4. Fill, drain, refill and tune

Record starting water height, safe maximum fill mark, catch-container free capacity, valve/drain setting, switch order, configuration revision and timing instrument. Check hoses and vessels for leaks before every cycle. Do not add a pump or change electrical plumbing to make this procedure work. Keep filling/draining confined to the wet area with electronics protected.

### Defaults to measure, not claimed calibrated values

| Setting                              | Current working value             | Meaning                                                                                     |
| ------------------------------------ | --------------------------------- | ------------------------------------------------------------------------------------------- |
| `sensors.poll_interval_ms`           | 50 ms                             | Input polling cadence                                                                       |
| `sensors.stable_for_ms`              | 200 ms                            | Five-bit pattern must remain unchanged before accepted level change                         |
| `sensors.stale_after_ms`             | 1000 ms                           | Old successful readings become unknown; steady unchanged water still gets fresh polls       |
| `interaction.resume_level`           | 1                                 | Minimum valid level for recovery                                                            |
| `interaction.refill_hold_ms`         | 2000 ms                           | Continuous valid recovery hold after stabilization                                          |
| `interaction.input_inactivity_ms`    | 120000 ms                         | Abandoned Input returns to Start                                                            |
| `interaction.finished_timeout_ms`    | 60000 ms                          | Finished session returns to Start                                                           |
| `config/script.json` progress delays | 120 seconds total active progress | Authored exhibition pacing, not the recording's actual duration; pauses extend elapsed time |

1. Begin below S1. Allow stabilization and verify level 0. Enter a synthetic idea and submit while dry: Running must show the refill interruption **before any progress**, not pretend water exists. Test unknown/fault entry separately with a safely controlled diagnostic condition; do not yank powered wires to create it.
2. Fill slowly past one switch at a time, pausing long enough for stable readings at each height. Record the observed indication against this **normalized wet** table; raw bits may differ because of inversion:

   | Wet pattern, S1 → S5     | Expected level                                                  |
   | ------------------------ | --------------------------------------------------------------- |
   | `00000`                  | 0                                                               |
   | `10000`                  | 1                                                               |
   | `11000`                  | 2                                                               |
   | `11100`                  | 3                                                               |
   | `11110`                  | 4                                                               |
   | `11111`                  | 5                                                               |
   | Any other stable pattern | Sensor fault, no valid level; never count isolated wet contacts |

3. Verify that crossing S1 briefly and dropping back does not resume an interrupted session. Hold at or above the configured `resume_level`, with valid stable sensing continuously for the configured hold. Observe automatic resume at the **same script position and remaining delay**, with no duplicated/skipped task or early summary/QR. With current defaults, the 200 ms stabilization precedes the 2-second recovery hold; polling/scheduling add latency, so record observed times rather than claiming exactly 2.200 seconds.
4. Fill only to the safe marked maximum, then drain through levels 5 → 0. Record each falling threshold and the elapsed drainage time. At stable level 0, Running must pause, append one water warning for the incident and freeze progress. Refill and repeat; at least three physical drain/refill cycles belong in acceptance. Interrupt near the final step as well: empty/faulty water must win over completion. Once already finished, later water changes update the indicator without starting another session.
5. At a threshold, observe natural movement/contact bounce and gently exercise the installed cable route without opening powered connections. Record whether changes shorter than the filter are rejected and stable changes accepted. A recovery hold must restart when water dips, sensing becomes invalid or readings do not remain stable; a continuously unchanged valid level must not become stale merely for being unchanged.
6. Verify an invalid contiguous-order condition only through safe isolated switch actuation that the mounting allows, with no powered rewiring. Progress must pause with a sensor warning; restoring valid level 0 leaves the session paused for water, while stable adequate water plus the hold resumes. If creating a physical fault is unsafe, leave that physical trial blocked and use the separate labelled mock acceptance procedure; mock evidence is not a measured cable-disconnection or GPIO-read-failure test.
7. Tune one parameter at a time, only after hardware faults are repaired. Record old/new values and the repeated result. Prefer correcting drain rate, vessel capacity or switch mounting safely to pretending water remains valid. Never bypass the level-zero pause, accept noncontiguous bits, disable stale detection or set `resume_level` to 0. Stop the service before editing local JSON and restart after review; configuration is loaded at process startup, not hot-reloaded. Coordinate any `progress[].delay_ms` changes with the copy owner so summary/provenance and the physical drainage performance remain consistent. Repeat the affected six-level, recovery and pacing trials after each change.

A disconnected wire can look like an open contact; depending on polarity this can resemble dry **or wet**. A stuck contact can also produce a plausible contiguous pattern. The software cannot certify every cable fault or detect overflow. Inspect the circuit and tank even when the display says water is available.

## 5. Bluetooth pairing, layout and recovery

Pair only during maintenance, with the real keyboard in its manufacturer's pairing mode and a recovery console available:

```sh
sudo systemctl enable --now bluetooth.service
sudo rfkill unblock bluetooth
bluetoothctl
```

In the interactive `bluetoothctl` prompt:

1. Enter `power on`, `agent KeyboardDisplay`, `default-agent`, then `scan on`.
2. Identify the actual keyboard in the scan. Enter `pair ACTUAL_DEVICE_ID`, replacing `ACTUAL_DEVICE_ID` with that observed identifier, and complete the displayed passkey/confirmation on the real keyboard as instructed. There is no sample address to paste.
3. Enter `trust ACTUAL_DEVICE_ID`, `connect ACTUAL_DEVICE_ID`, then `info ACTUAL_DEVICE_ID`. Confirm paired, trusted and connected status.
4. Finish with `scan off`, `discoverable off`, then `quit`. Do not publish the identifier or passkey in evidence. If authorization fails, use the maintenance administrator, not a root kiosk process.

For an already bonded keyboard, **do not re-pair first**: wake it, check battery/charge and range, check `rfkill list` and `systemctl status bluetooth.service`, then use `bluetoothctl` → `power on` → `info ACTUAL_DEVICE_ID` → `connect ACTUAL_DEVICE_ID`. Re-enter the app and test synthetic input. If the daemon itself is failed, inspect `journalctl -u bluetooth.service --since today` and resolve the cause; an intentional `sudo systemctl restart bluetooth.service` during maintenance disconnects other Bluetooth devices and is not a routine first step.

If the bond is irrecoverably stale, warn that re-pairing removes that connection, keep the recovery console working, then enter `remove ACTUAL_DEVICE_ID` in `bluetoothctl`. Put the keyboard back in pairing mode and repeat the full scan/pair/trust/connect sequence. Never remove every stored device or delete the BlueZ state directory as a shortcut. BlueZ pairing can replace an existing bond; use `connect` for ordinary reconnection.

Configure the physical console with `sudo dpkg-reconfigure keyboard-configuration`. Separately record/approve the actual Qt keyboard layout: Weston uses `[keyboard] keymap_layout` and any required variant; EGLFS uses the approved XKB layout supported by its lifecycle. Test uppercase, punctuation, language-specific characters, backspace and ENTER in the app; console typing alone is not acceptance. Changing layout requires the corresponding approved display configuration and lifecycle reinstall, not just a console setting.

Record keyboard model/layout and measured recovery latency for natural sleep/wake, keyboard power cycle, Pi reboot, and boot with keyboard absent followed by connection. Missing/sleeping input must not block or crash startup. Do not globally defeat keyboard sleep or log input events to conceal a reconnect defect.

## 6. Offline startup, daily opening and next visitor

Only after supervised display, sensor, service/recovery and copy/URL acceptance is complete, stop the service and repeat the full recorded selection with **both `--apply --enable`** to authorize boot. For the approved Wayland/live route:

```sh
sudo systemctl stop thirsty.service
sudo /usr/bin/python3 deploy/systemd/install.py --display-backend wayland --mode live \
  --approval /root/thirsty-maintenance/approval.json \
  --display-config /root/thirsty-maintenance/weston.ini --apply --enable
sudo systemctl start thirsty.service
```

This installs/enables but does not start until the separate `start` or next boot. Backend changes need new physical approval; mock is never an automatic recovery mode.

With local maintenance access preserved, disable **Wi-Fi only**:

```sh
sudo rfkill block wifi
rfkill list
```

Confirm Bluetooth remains unblocked/connected. Never use `rfkill block all`, `rfkill unblock all`, `dtoverlay=disable-bt` or a Bluetooth service stop as an offline policy. If this image uses NetworkManager, its Wi-Fi-only setting is an alternative described in `device.md`; do not assume the command exists. Prove the chosen Wi-Fi policy persists across a safe reboot and cold start; do not assume rfkill state survives. `sudo rfkill unblock wifi` is for intentional maintenance, not visitor startup.

At opening:

- Inspect tank, catch-container capacity, dry electronics, cables and power leads; set only the approved water/drain arrangement. Stop if there is leakage, unexpected warmth, damaged insulation or unexplained sensor indication.
- Power the display/Pi according to the recorded arrangement. Confirm a fresh fullscreen **Start** screen with no desktop dialogs, terminal/getty or restored visitor transcript. Check water indication against the actual tank, not just the last recorded fill.
- Wake/type with the keyboard and run one synthetic journey, including the expected refill behavior. Check that app and local QR work without Wi-Fi. Phone Internet is a separate requirement for opening the URL.
- At Finished, a **fresh ENTER press** or the configured 60-second default returns to Start and clears the session. Do not hold ENTER across transitions. Abandoned Input resets after the configured 120-second default. Running and paused sessions have no inactivity reset: refill/recover normally or use the operator restart below to abandon deliberately.

For an operator reset at any point:

```sh
sudo systemctl restart thirsty.service
```

This abandons the current idea/transcript/timers, rereads sensors and starts at Start. It does not empty/fill the tank, repair a sensor or change Bluetooth bonds. Tell the visitor before abandoning a session. There is no undocumented keyboard reset shortcut.

## 7. Fault recovery and maintenance controls

First ensure people and water/electrical equipment are safe. With leakage into electronics, smoke or electrical danger, keep people away and isolate power from a safe dry upstream disconnect according to the venue's emergency procedure; do not touch wet hardware or prioritize orderly software shutdown over safety. Do not re-energize until a competent person clears it.

For a nonhazardous software/sensor issue:

```sh
systemctl status thirsty.service
journalctl --namespace=thirsty -u thirsty.service --since today
sudo systemctl stop thirsty.service
```

Logs are bounded and volatile in the **thirsty namespace**; a reboot may remove them. Save only necessary, reviewed operator diagnostics privately before reboot, never visitor text, input traces, broad environment dumps or visitor screenshots. Do not enable verbose Qt input logging during exhibition use.

| Symptom                                                                            | Recovery action and return-to-service condition                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Refill warning at level 0                                                          | Inspect actual water/catch capacity, refill safely above the approved threshold, then wait for stabilization plus the recovery hold. Do not restart merely to skip the warning.                                                                                                                          |
| Sensor fault/unknown, impossible level, or water indication inconsistent with tank | Stop the session/service. For physical inspection use safe shutdown and remove power before touching connectors. Recheck S1–S5 order, polarity, cable continuity, dry protection and measurements. Restore valid readings and verify a full recovery; plausible values alone do not prove wiring intact. |
| Sleeping/disconnected keyboard                                                     | Follow §5; app startup must not depend on a connected keyboard. Restarting the app is not pairing.                                                                                                                                                                                                       |
| Black/blank screen or repeated display failure                                     | Use recovery console, stop service, inspect namespace logs, HDMI power/mode, active seat/VT, approval/config and competing display/getty. Fix the recorded route; never switch backend, software renderer or root permissions silently.                                                                  |
| Repeated service restart / start limit                                             | Read the failure first and stop. Fix invalid config, missing packages, permissions or hardware cause. Then `sudo systemctl reset-failed thirsty.service` and `sudo systemctl start thirsty.service`. Do not repeatedly clear the limit to conceal a fault.                                               |
| Process failure or power restoration                                               | Expected behavior is a new Start, not a restored transcript. If this does not occur, stop admission and diagnose. A manual `systemctl stop` intentionally stays stopped.                                                                                                                                 |
| Configuration/URL error                                                            | Restore the reviewed complete local JSON or correct the actual field named by the error. Never insert a sample URL, force full water, loosen validation or copy a fixture into production.                                                                                                               |
| OOM, sustained swapping, thermal/voltage warning or sluggish typing                | Stop admission and collect target resource/power evidence through `device.md`. Fix supply/cooling/package/display issues; a 512 MB Pi must pass measured resource acceptance before reopening.                                                                                                           |

The service bounds repeated failure (four starts in 120 seconds, five-second restart spacing). Only resume after the underlying cause is corrected and a supervised synthetic journey passes. Explicit stop permits orderly app/GPIO cleanup; do not habitually use `kill -9`, pull the SD card or yank power as recovery.

## 8. Safe shutdown, updates and rollback

For a normal closing or hardware adjustment:

1. Tell the visitor the session will end; restrict filling and secure the water/drain arrangement. Keep mains and electronics dry.
2. From maintenance access, stop the service, save needed volatile evidence, then request OS shutdown:

   ```sh
   sudo systemctl stop thirsty.service
   sudo systemctl poweroff
   ```

3. Wait for shutdown completion using the recorded local console/activity indication; a blank HDMI screen alone is not proof the OS halted. Only then disconnect Pi/display power in the documented order. Remove all possible supplies before touching GPIO, moving water near electronics, removing the card or altering cables. Normal shutdown is not the emergency spill procedure.

For updates, close to visitors, back up the accepted card first, record the known-good revision/config/package evidence and stop the service. Use the official signed package plan procedure and a reviewed complete source/assets/config revision, preserving root ownership and read-only kiosk access. Never pull unreviewed code at boot, modify the recorded experiment, generate an app in `output/app`, restore a workstation `.venv` or perform an unreviewed distro upgrade.

If package, display, pin or timing changes invalidate approval, revoke the affected assertion and repeat those physical trials. Re-run preflight with fresh evidence filenames. Reinstall through the full selected lifecycle command **without `--enable`** for the supervised update trial; it leaves boot disabled. If the namespace journald configuration changed while active, stop the kiosk and intentionally run `sudo systemctl restart systemd-journald@thirsty.service` before the next trial. The helper does not restart it automatically or alter the host's global journal policy. After successful acceptance, repeat with `--apply --enable`.

To prevent boot into a broken installation:

```sh
sudo systemctl disable --now thirsty.service
```

Restore the known-good image or complete approved source/config/package state, not arbitrary individual files from different revisions. If removing lifecycle files rather than restoring an image, follow the exact **Stop and rollback** section in `deploy/systemd/README.md`, preserving pre-existing files and the prior VT7/getty state. The installer is not transactional; a failed apply needs inspection before retrying. Do not remove common packages, reset all radios or delete Bluetooth bonds as a kiosk rollback.

## 9. Full-card backup and recovery image

A copy of the application alone does not preserve the approved OS/packages, boot setup, service, display configuration, keyboard bonds or permissions. Back up a known-good, safely shut down card, before updates and after final commissioning. Never image a mounted, running Pi root filesystem and call it a consistent backup.

1. Shut down using §8, disconnect power and remove the card. On a **separate Linux maintenance computer**, identify the removable card by size/model and insertion, using:

   ```sh
   lsblk -o NAME,SIZE,MODEL,TYPE,MOUNTPOINTS
   ```

   Verify the whole-card device against the physical card twice; it must not be the maintenance computer's system disk. Unmount each listed card partition with `sudo umount` followed by its actual partition path. Do not unmount unrelated disks. The backup command below uses GNU/Linux `dd`, not macOS/BSD options.

2. Set shell variable `CARD` to the observed **whole-card block-device path**, not a partition, and `IMAGE` to a **new absolute image filename** on separate trusted storage with at least the card's capacity free. No device name is supplied here because guessing one risks the wrong disk. Set these variables in the same maintenance shell before the commands:

   ```sh
   : "${CARD:?Set CARD to the independently identified whole-card device}"
   : "${IMAGE:?Set IMAGE to a new absolute backup image path}"
   test -b "$CARD" && sudo dd if="$CARD" of="$IMAGE" bs=4M iflag=fullblock conv=excl,fsync status=progress
   ```

   `CARD` is the input; `IMAGE` is the output. `conv=excl` refuses an existing output, but it cannot protect against a wrongly identified source. Stop on any error. After a successful copy, calculate and record the image hash:

   ```sh
   sudo sha256sum "$IMAGE"
   ```

3. Record image date, hash, card capacity, project/config revision, OS/package report and approval evidence together. Protect the image as a credential-bearing secret: it includes Wi-Fi material, Bluetooth bonds, system identities and maintenance keys. Keep access restricted, retain a separate known-good copy and do not commit or place it in `output/app`. No persistent visitor session is needed for recovery; do not start logging visitors to enrich the backup.
4. Prove recovery on a **spare card of sufficient actual byte capacity**, retaining the original untouched. On the maintenance computer, select the saved image through Raspberry Pi Imager's custom-image option, independently identify the spare target, acknowledge that it will be erased, and let write verification complete. Recalculate/compare the stored image hash before use. Nominally identical card sizes do not guarantee identical capacity.
5. Insert the spare only while the Pi is off. Reconnect the recorded safe hardware and cold boot offline. Verify actual Start/fullscreen, chosen route, keyboard sleep/reconnect, live six-level/refill behavior and service restart before declaring the image recoverable. Record the observed result and recheck any changed hardware approval. A cloned card reproduces machine credentials and bonds; use it only for this installation, not simultaneously in another public device. If no trusted image restores correctly, rebuild from the recorded official image and repeat commissioning; do not claim a recovery pass.

## 10. Release handoff

Keep the installation closed until TH-02/08/10 physical gates and TH-11 acceptance are recorded, including the eight-hour run, at least 100 automated mock sessions plus three physical drain/refill cycles, boot/recovery, keyboard behavior, resource observations and actual-screen legibility. These are required future observations, not results reported by this runbook.

Have the owner approve the exact final screen/transcript/summary/refill/fault copy and pacing revision. The configured owner URL is **https://zwei.berlin/app-repo**; its redirect is still pending. The owner must configure it to the intended pre-existing repository and verify the destination; then scan the completed local QR on the actual HDMI display with a connected phone, check the readable URL and confirm the expected repository opens. Do not replace the URL with a test fixture, invent an available repository or call a local QR an online handoff pass. The installation interaction stays offline; the phone's link-opening check requires connectivity.

Handover includes this runbook, private dated wiring/measurement and backend approval records, known-good configuration/revision and image hash, physical acceptance evidence, recovery access and the operator's practiced stop/restart/refill/keyboard/shutdown sequence. Any remaining unmeasured item stays explicitly blocked; `output/app/` stays empty and the recorded experiment stays unchanged.
