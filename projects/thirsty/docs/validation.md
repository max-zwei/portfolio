# Validation evidence

## Scope and release status

Native Python/PySide6/Qt Quick kiosk software is implemented. This report records checks performed by the integration owner, not new checks run during documentation editing. No Raspberry Pi or physical installation hardware was available. TH-01/03/04/05/06/07/09 are software-complete, including the final native entry-point QR smoke. TH-02/08/10 remain physically BLOCKED despite implemented deployment/calibration tooling. TH-11 mock work is complete; physical acceptance and owner approval remain BLOCKED.

## Workstation environment

| Item              | Observed version |
| ----------------- | ---------------- |
| OS / architecture | macOS 27, arm64  |
| Python            | 3.14.8           |
| Qt / PySide6      | 6.12.0           |
| segno             | 1.6.6            |

These are workstation observations, not an approved Pi image or package baseline.

## Earlier workstation checks

- **364 tests passed in 2.50 seconds** in the earlier workstation suite, including 18 deployment tests. Deployment regressions are portable workstation tests, not Linux/Pi runtime proof.
- The editable wheel built and installed successfully with pip; the installed `thirsty --help` entry point returned the supported CLI options.
- **98 runtime Theme values** matched DESIGN. `app/ui/Theme.qml` is the native full-token mapping; no browser `tokens.css` is used.
- Script provenance: **28 source events and 43 quotes** checked against source evidence.
- Native screen journeys exercised pause, refill, finish, reset and uniform scaling/letterboxing.
- An actual **QTimer refill-hold smoke** exercised the real timer path, rather than only fake-clock unit tests.
- Deployment syntax, plan generation and refusal to apply on the unsupported workstation host were checked. This is not evidence of installation or service startup on a Pi.
- Corrected installer plans and unsupported-host apply refusals passed for both explicit display routes. Local links in eight documentation files, syntax of 31 shell examples and one embedded Python diagnostic passed; hardware examples were not executed.
- QML static lint reported the ambient `controller` context in `Main.qml`; this is a static context-resolution warning. Native Qt smoke runs emitted no runtime Qt warnings.
- **Final integrated native QR smoke passed**, with the actual `app.main.main` entry point and no production-component mocks. Cocoa native keyboard `a`/ENTER input covered start and submit; an external raw JSON file drove mock sensing. Real Qt timers, sensor stabilization and the two-second refill hold were exercised. All 18 stages completed with temporary 100 ms stage delays. zxing-cpp independently decoded the QR from the final rendered window screenshot as exactly `https://zwei.berlin/app-repo`. Reset and clean exit passed without Qt runtime warnings.
- Smoke limitations: the host window became inactive/unexposed mid-run, so explicit frame grab/polish was used and final reset invoked the controller slot. An earlier screen-level native smoke separately verified finished-screen ENTER reset. This is not an uninterrupted physical-display interaction test, a phone scan or proof that the URL destination is published.

### Deployment review corrections

Code review identified five concrete deployment defects, now corrected in the implementation:

1. The service's AF_UNIX-only restriction prevented Weston's udev netlink access. The service now allows AF_UNIX and AF_NETLINK while continuing to deny INET/INET6.
2. lgpio notification files would use an immutable working directory. The child receives `LG_WD=/run/thirsty`, a private writable runtime directory.
3. Weston's default input requirement could prevent startup with the keyboard disconnected. The configuration gate and deployment instructions now require `core.require-input=false`.
4. The root installer could import installed validation code or execute preflight before checking its integrity. It now checks root ownership, absence of group/world writes and absence of symlinks for ancestors and the entire application tree before validation.
5. PAM/logind children may leave the service cgroup, allowing application/Weston processes to survive a supervisor SIGKILL. Both launches now use fresh-interpreter exec wrappers that arm `PR_SET_PDEATHSIG=SIGKILL` and verify the expected parent PID to close the setup race.

These are implementation corrections, not physical deployment acceptance. Parent-death handling covers direct non-setuid children, not arbitrary daemonizing grandchildren; SIGKILL cannot run Python GPIO cleanup. Actual Pi/systemd/VT/DRM behavior, netlink hotplug, lgpio runtime operation, keyboard-disconnected reboot and device release after SIGKILL remain unverified.

## User-feedback verification

The integration owner verified the feedback changes on the macOS workstation after clearing recurring local hidden Qt plugin flags; documentation editing did not rerun these checks.

- **364 tests passed in 2.69 seconds.**
- An actual Cocoa QML journey exercised the output plan with the typed visitor idea, water interruption, refill and completion, with no Qt runtime warnings.
- Transcript geometry was observed at x96/y96 with a 528px viewport height on the 1280 × 720 reference canvas, preserving 96px beneath the viewport.
- Running-icon animation advanced in discrete 100ms steps through indices 1, 2, 3 and 4; disabling it reset the animation.
- Visual inspection of Start and plan captures confirmed the magenta heading, transparent avatar and intended padding.
- Start, Input, water-paused and finished captures were updated; plan and action captures were added below.

These checks establish workstation feedback behavior, not physical Pi acceptance, publication of the repository destination or a new 100-session run. The earlier accelerated-session evidence remains separate below.

## 100 accelerated mock sessions

Before the user-feedback changes, the integration owner exercised the actual QML interface, controller and mock sensor adapter for **100 sessions**, using the default **120-second active script**. Every session included both a dry-water pause and an invalid-pattern sensor pause. Checks covered exactly-once progress and summary insertion and clearing session state on reset. This run was not repeated for the feedback changes.

- Wall time: **4.55 seconds**.
- Simulated elapsed time: **12,955 seconds**.
- This is accelerated simulated time, not a real-time soak.

| Completed sessions | Workstation RSS (KiB) |
| ------------------ | --------------------: |
| 20                 |               168,544 |
| 40                 |               169,776 |
| 60                 |               170,256 |
| 80                 |               171,072 |
| 100                |               171,600 |

RSS rose by 3,056 KiB between the first and last recorded samples. This is a small observed rise, **not proof of bounded memory or absence of leaks**. There was no eight-hour soak and no Pi memory measurement. These workstation values do not establish compatibility with the Pi 3 Model A+'s 512 MB RAM.

## Native captures

The integration owner supplied updated native captures for the user-feedback verification. Start, Input, water-paused and finished replace the earlier captures; plan and actions are additional views:

| State                      | Capture                                         |
| -------------------------- | ----------------------------------------------- |
| Start                      | [start.png](validation/start.png)               |
| Input                      | [input.png](validation/input.png)               |
| Output plan / visitor idea | [plan.png](validation/plan.png)                 |
| Mixed tasks / actions      | [actions.png](validation/actions.png)           |
| Water paused               | [water-paused.png](validation/water-paused.png) |
| Finished / QR              | [finished.png](validation/finished.png)         |

Workstation screenshots do not replace installed-screen checks, pixel/QR readability at the actual display mode or a phone scan.

## Approval and physical acceptance still required

- Owner copy review is pending. Software implementation does not require further confirmation to proceed.
- The chosen URL is `https://zwei.berlin/app-repo`; redirect publication is pending and `output/app/` is empty. Rendering or encoding that URL does not establish a usable app destination.
- Verify passive contacts before GPIO wiring; measure actual wet/dry polarity, bottom-to-top order, cable behavior and final pin map. Unverified configured pins remain provisional.
- Record actual Pi OS/packages, graphics backend, display mode, power arrangement, keyboard pairing/layout/reconnect and GPIO permissions.
- Exercise cold boot, process crash/restart, Wi-Fi-off operation with Bluetooth retained, keyboard sleep/reconnect and absence of obstructing desktop dialogs.
- Complete physical calibration and at least three drain/refill cycles; tune timing to actual drainage.
- Complete an eight-hour real-time installation soak, measure Pi memory/swap and assess any increasing trend.
- Scan the final published destination from the installed HDMI display with a phone.

See [PRODUCT release checklist](../PRODUCT.md#7-approval-and-installation-release-checklist), [device setup](device.md) and [operator procedures](operator.md). None of the physical checks above has been performed.
