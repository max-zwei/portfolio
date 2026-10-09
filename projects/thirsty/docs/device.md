# Device baseline — TH-02

## Scope and current evidence

Selected hardware is **Raspberry Pi 3 Model A+, 512 MB**, HDMI at **1280 × 720**, a Bluetooth keyboard and five passive JO-GL534 contacts. Selected software is **Raspberry Pi OS Lite 32-bit, Trixie**, its system Python and packaged PySide6/Qt Quick/QML, Segno, GPIO Zero and lgpio. A 64-bit kernel with **32-bit armhf userspace** is acceptable; `uname -m` alone is not an architecture check.

**No Pi is available. No physical installation, package transaction, graphics test, power/memory measurement, keyboard reconnect or wiring verification has been performed. TH-02 physical acceptance remains blocked.** The tooling is an operator procedure, not proof of compatibility. Do not connect switches or run live mode on the strength of a package install or preflight report. Unknown pins, physical pin numbers and tested backend remain null in `config/device.json`; `hardware_verified` remains false. No generated app is installed in `output/app`.

## Supported package selection and primary sources

Use a fresh official Trixie Lite **32-bit** image, not Bookworm/Legacy, desktop images, a distro upgrade in place, a 64-bit image or a mix of Debian suites. Raspberry Pi OS documents its [Trixie basis and Lite variants](https://www.raspberrypi.com/documentation/computers/os.html); download through [Raspberry Pi's OS distribution](https://www.raspberrypi.com/software/operating-systems/). The [Pi 3 A+ product brief](https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-a-plus-product-brief.pdf) specifies 512 MB and a 5 V/2.5 A supply. This is a specification, not a measurement of the installation supply.

Package research below was made against official Debian and Raspberry Pi repositories. Repository versions can change; **the target's `apt-cache policy` and installed evidence are authoritative**, not these reference versions. Keep the image's official signed repository configuration. If a package is absent, stop; do not add an arbitrary repository, download guessed `.deb` files, disable signature checking, build Qt on the 512 MB Pi or substitute a pip wheel.

| Requirement              | Packages / supported version                                                                                                                              | Official evidence                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Python and bindings      | System `/usr/bin/python3`, Python ≥3.11; `python3-pyside6.qtcore`, `.qtgui`, `.qtqml`, `.qtquick`, `.qtsvg`; PySide6 and Qt ≥6.8, <7                      | [Trixie Qt Quick binding](https://packages.debian.org/trixie/python3-pyside6.qtquick) is 6.8.2.1-4 with armhf builds; [QtSvg binding](https://packages.debian.org/trixie/python3-pyside6.qtsvg). Binding packages pull matching Qt libraries.                                                                                                                                                                      |
| QML runtime imports      | `qml6-module-qtqml`, `-qtqml-models`, `-qtqml-workerscript`, `-qtquick`, `-qtquick-window`, `-qtquick-layouts`, `-qtquick-controls`, `-qtquick-templates` | [Official Qt Declarative binary package list](https://packages.debian.org/source/trixie/qt6-declarative), Qt 6.8.2. Python bindings alone do not install every QML import. Custom UI components do not imply the import plugins can be omitted.                                                                                                                                                                    |
| SVG images               | `libqt6svg6`, **`qt6-svg-plugins`**, `python3-pyside6.qtsvg`                                                                                              | [SVG library contents](https://packages.debian.org/trixie/armhf/libqt6svg6/filelist) versus [SVG plugin contents](https://packages.debian.org/trixie/armhf/qt6-svg-plugins/filelist): `libqsvg.so` is in the latter, required for QML SVG Image loading.                                                                                                                                                           |
| Local QR                 | `python3-segno` ≥1.6, <2                                                                                                                                  | [Debian Segno](https://packages.debian.org/trixie/python3-segno), reference 1.6.6-2, pure Python/local encoding.                                                                                                                                                                                                                                                                                                   |
| Digital inputs           | `python3-gpiozero` ≥2, <3 and `python3-lgpio` ≥0.2.2 from the **Raspberry Pi repository**                                                                 | [Pi GPIO Zero archive](https://archive.raspberrypi.com/debian/pool/main/g/gpiozero/) supplies 2.0.1-0+rpt1+trixie; [Pi lg-gpio archive](https://archive.raspberrypi.com/debian/pool/main/l/lg-gpio/) supplies python3-lgpio 0.2.2-1~rpt1+trixie for armhf. [Debian GPIO Zero](https://packages.debian.org/trixie/python3-gpiozero) is only 1.6.2; Debian alone is not this baseline. No pigpio daemon is required. |
| Graphics libraries       | `libqt6gui6`, `libegl1`, `libegl-mesa0`, `libgles2`, `libgbm1`, `libgl1-mesa-dri`                                                                         | [Qt GUI](https://packages.debian.org/trixie/libqt6gui6), [Mesa EGL](https://packages.debian.org/trixie/libegl-mesa0), [Mesa DRI](https://packages.debian.org/trixie/libgl1-mesa-dri). Keep the image's VC4 KMS/Mesa stack; no legacy proprietary Broadcom EGL route.                                                                                                                                               |
| Explicit Wayland route   | `qt6-wayland`, `weston` in addition to common packages                                                                                                    | [Wayland armhf plugin list](https://packages.debian.org/trixie/armhf/qt6-wayland/filelist) includes `libqwayland-egl.so`; [Weston](https://packages.debian.org/trixie/weston) reference 14.0.2-1 supports armhf and DRM. No Xwayland or desktop shell needed.                                                                                                                                                      |
| Keyboard and diagnostics | `bluez`, `rfkill`, `keyboard-configuration`, `console-setup`, `xkb-data`, `procps`, `util-linux`                                                          | [BlueZ commands](https://manpages.debian.org/trixie/bluez/bluetoothctl.1.en.html), [keyboard configuration](https://packages.debian.org/trixie/keyboard-configuration), [procps](https://packages.debian.org/trixie/procps), [util-linux](https://packages.debian.org/trixie/util-linux). Pi image tools such as `vcgencmd` are reported if present, never assumed.                                                |

`deploy/packages.txt` is the common manifest. The installer adds only `qt6-wayland weston` when explicitly requested. It deliberately does **not** advertise `qt6-qpa-plugins` as an EGLFS installer: the [Trixie armhf QPA file list](https://packages.debian.org/trixie/armhf/qt6-qpa-plugins/filelist) contains VNC, and the [Qt GUI file list](https://packages.debian.org/trixie/armhf/libqt6gui6/filelist) contains no EGLFS plugin. Those packages do not establish the preferred EGLFS/KMS route. No invented `qt6-eglfs` package is used.

The preferred architecture remains EGLFS/KMS **only if the actual official Pi Qt build exposes and successfully runs it**. With the documented Debian package contents, the available packaged alternative is **explicitly selected Wayland/Weston kiosk**, still requiring physical validation. There is no automatic EGLFS → Wayland → software-renderer fallback. A plugin filename or successful import is not a render test.

## Operator installation, without automatic service setup

1. Download the selected official image, verify its published SHA-256, and record the exact filename, release date, download URL, published hash and independently calculated hash in the installation record below. Flash using Raspberry Pi Imager and verify the write. Configure a private maintenance identity and locale. Do not place passwords, Wi-Fi credentials, Bluetooth addresses or visitor ideas in committed evidence.
2. Boot with the HDMI screen and safe power supply attached; keep all switches **disconnected from the Pi**. Preserve a local recovery keyboard/console before disabling any network access. Inspect the image's existing VC4 KMS setup before changing it. This procedure does not rewrite `/boot/firmware/config.txt` or `cmdline.txt`.
3. Copy a complete, reviewed project checkout (including local assets/config) to the device. The later service contract uses `/opt/thirsty`; application/config files should be operator-owned and read-only to the kiosk identity. Run commands below from that checkout. No pip install is needed; `/usr/bin/python3 -m app.main` uses packaged modules directly. Do not copy the workstation `.venv` to the Pi.
4. On the **Pi only**, with maintenance networking available, refresh the signed package index and review candidates. Choose Wayland explicitly for the package-supported route, or request EGLFS only when investigating a verified packaged EGLFS build:

   ```sh
   sudo apt-get update
   bash deploy/setup-device.sh --display-backend wayland
   ```

   Default invocation performs target guards, prints candidate versions and runs `apt-get --simulate --no-install-recommends --no-remove`. It does not install. Missing candidates, out-of-range PySide6/GPIO Zero/Segno, wrong board, OS or architecture stop the procedure. Review disk space and dependency changes. The installer neither switches repositories nor updates the index itself.

5. After review, explicitly authorize the package transaction:

   ```sh
   sudo bash deploy/setup-device.sh --display-backend wayland --apply
   ```

   This recomputes and displays current candidates, simulates the exact version-selected transaction, then asks apt's normal confirmation. Repeating it is safe when candidates are unchanged; with changed indices it may upgrade dependencies, so compare the plan each time. There is no unattended `-y`, package removal, service unit installation, user creation, GPIO action, radio change or reboot in this script. OS package maintainer scripts may start their normal services; inspect the transaction. Back up the accepted image before later updates.

6. Inventory offline as a **non-root** user, and repeat as the final kiosk identity/session once TH-08 supplies it:

   ```sh
   /usr/bin/python3 deploy/preflight.py --display-backend wayland --require-pi --require-software --output /tmp/thirsty-baseline.json
   ```

   Use a new evidence filename each time. `--help` works on the workstation without Qt, GPIO or Linux device files; a full workstation report is allowed but cannot pass Pi eligibility. Nothing here authorizes live wiring.

## Preflight contract and evidence limitations

`python3 deploy/preflight.py [--display-backend eglfs|wayland] [--device PATH] [--pid PID] [--output PATH|-] [--require-pi] [--require-software]`:

- Defaults to JSON on stdout and exit 0 for an inventory, even when hardware/packages are absent. `--require-pi` returns **2** unless model, Linux Trixie, armhf package architecture and 32-bit interpreter match; `--require-software` returns **2** unless the selected software inventory matches. Argument errors also return 2. File creation failure returns 1. `--output` creates a new mode-0600 file and refuses overwrites; parent directory must already exist.
- Records kernel/model/OS/architecture; Python and distribution/package versions; Qt runtime version, QML module and QPA/EGL integration/SVG filenames; selected display environment, DRM advertised modes, node permissions; current UID/groups; known sensor configuration; memory/swap and optional application memory counters; power/temperature/rfkill/Bluetooth-service and active-session diagnostics. No network access is made.
- The optional `--pid` reads only memory/thread counters, never command lines, environment, process contents, transcript or visitor text. Record it during synthetic idle/typing runs. Preflight does not enumerate Bluetooth peers, capture input, inspect browser state, collect machine serials or dump arbitrary application config. Device/session paths and package errors are operator information; still review reports before publishing.
- It imports Qt binaries in a bounded child process **without a QGuiApplication/window**. GPIO libraries are discovered via module metadata only. No pin factory or `DigitalInputDevice` is constructed; no `/dev/gpiochip*`, input event or DRM device is opened. Node listing and sysfs reads are passive, not modesetting.
- Missing diagnostic commands or unreadable resources are `unavailable`/`error`, not a fabricated passing value. `vcgencmd get_throttled` absence is a blocker to that evidence, not proof of good power. Per-command timeout is 15 seconds. No sudo escalation occurs.
- `target_eligible`, `software_baseline_eligible` and `selected_backend_plugins_present` are **inventory flags**, not deployment approval. `physical_acceptance_verified` is always false. Config `hardware_verified` is labelled as an operator assertion, not independently established safety. Advertised 720p does not establish actual scanout mode, and plugin presence does not establish ABI loading, GPU acceleration, input or session ownership.

## Display route, seat and permissions

Use the image's current **full VC4 KMS** graphics stack. Do not copy obsolete `fkms`, legacy firmware `hdmi_group`/`hdmi_mode`, guessed DRM card indices, forced memory splits or unsafe overclock settings from old tutorials. Read [Raspberry Pi display/KMS guidance](https://www.raspberrypi.com/documentation/computers/configuration.html) and [Qt 6.8 embedded Linux](https://doc.qt.io/qt-6.8/embedded-linux.html). Check the actual HDMI connector and its EDID-advertised 1280 × 720 mode. Select that physical mode in the chosen backend; app logical width/height alone do not change HDMI scanout. If unavailable, record the blocker; only the product's uniform 16:9 letterboxing rule is allowed, subject to actual QR/legibility acceptance.

**Ownership is not solved by `sudo` or `chmod 666`:** the kiosk must be a dedicated non-root `thirsty` identity. TH-08 owns its creation, VT/session and boot lifecycle. `/dev/dri/card*` access and DRM master/active seat are required by the direct display owner; `/dev/dri/renderD*` is not a substitute for modesetting authority. Input nodes must be readable by the display owner, GPIO chip nodes accessible only when live sensing is authorized. On this image these are normally controlled through logind/udev and groups such as `video`, `render`, `input` and `gpio`; inspect actual ownership first. Group membership changes require a new session. Do not grant sudo, broad device capabilities or root to the app. `input` access exposes keystrokes: grant it only to the exclusive kiosk identity when needed.

Only one process/session can own the display seat at a time. For a manual trial, start from an active local VT in a non-root login session; do not assume an SSH session, `sudo -u` or a background system service creates an active logind seat. There must be no competing desktop/compositor. The eventual service must own a reserved VT and prevent a competing getty/shell from receiving visitor keystrokes; do not enable `QT_QPA_ENABLE_TERMINAL_KEYBOARD`. Reserve that work for TH-08, not this package script. Preflight as root cannot prove non-root permissions.

### Preferred EGLFS/KMS, conditional on actual packaged support

Before attempting launch, preflight must show both `platforms/libqeglfs.so` and `egldeviceintegrations/libqeglfs-kms-integration.so`. If either is absent, stop this route; explicitly choose/install Wayland rather than trying a guessed package or custom Qt compilation. If present, confirm shared-library loadability and the real DRM/input permissions on the Pi.

The operator supplies a trusted `/etc/thirsty/eglfs.json`, with `device` set to the **observed** DRM card path and an `outputs` entry whose `name` is the **Qt-reported** HDMI connector name and `mode` is `1280x720`. Qt connector names may differ from kernel sysfs names. Record the file and selected mode; no physical identifiers are prefilled here. See Qt's linked KMS JSON format. Run from the active VT, as non-root, with no compositor:

```sh
env -u DISPLAY -u WAYLAND_DISPLAY QT_QPA_PLATFORM=eglfs \
  QT_QPA_EGLFS_INTEGRATION=eglfs_kms \
  QT_QPA_EGLFS_KMS_CONFIG=/etc/thirsty/eglfs.json QSG_RHI_BACKEND=opengl \
  /usr/bin/python3 -m app.main --mode mock --fullscreen
```

This is a manual trial, not a boot command. No `--mode live` until the sensor gate below passes. Do not set `QT_QUICK_BACKEND=software` to hide GPU failure. Disable console blanking for the trial with `setterm --blank 0 --powersave off --powerdown 0` **on the owned local VT**, not over an SSH pseudo-terminal. Record unsupported `setterm` options instead of ignoring errors; the service/boot owner must later persist the supported blanking policy (for example the kernel `consoleblank=0` setting). Also disable the monitor's own sleep timer and prove a prolonged idle display remains visible.

### Explicit packaged alternative: Wayland / Weston kiosk

This is a display compositor, not a second Python application, browser or server. All experience logic remains one Python process/Qt loop. `qt6-wayland` alone is not a compositor. Weston and Qt must run as the same dedicated non-root session owner with a valid, private mode-0700 `XDG_RUNTIME_DIR`, normally created by PAM/logind under `/run/user/UID`. Do not invent a global `/tmp` runtime directory or use another user's socket. The compositor owns DRM/input; the Qt app connects to its socket.

Create `$HOME/.config/weston.ini` in the trial identity's home using the installed [weston.ini(5)](https://manpages.debian.org/trixie/weston/weston.ini.5.en.html) format: `[core]` has `shell=kiosk-shell.so`, `idle-time=0`, `xwayland=false`, `require-input=false`; `[output]` has `name` equal to the **observed Weston connector**, `mode=1280x720`, `scale=1`; `[keyboard]` has `keymap_layout` (and variant if needed) matching the actual keyboard. `require-input=false` allows startup with the Bluetooth keyboard disconnected; later input hotplug must still be physically verified. These are operator-filled settings, not a fabricated connector or layout. Do not use `--width/--height` for DRM: those options target nested/headless backends, not physical KMS output.

From the active local VT, after confirming no competing display owner, launch the installed Weston 14 route explicitly:

```sh
weston --backend=drm --renderer=gl --shell=kiosk-shell.so \
  --idle-time=0 --socket=thirsty-wayland --config="$HOME/.config/weston.ini"
```

`--renderer=gl` deliberately avoids an unproven automatic pixman/software fallback. In another operator shell under the **same session identity and runtime directory**, launch the app only once the compositor reports readiness:

```sh
env -u DISPLAY -u QT_QPA_EGLFS_INTEGRATION -u QT_QPA_EGLFS_KMS_CONFIG \
  WAYLAND_DISPLAY=thirsty-wayland QT_QPA_PLATFORM=wayland QSG_RHI_BACKEND=opengl \
  /usr/bin/python3 -m app.main --mode mock --fullscreen
```

A second SSH shell does not inherit the runtime directory automatically; use the verified same-user session environment, not a guessed socket. If DRM/logind or acceleration fails, stop and record it; do not run Weston as root. [Weston(1)](https://manpages.debian.org/trixie/weston/weston.1.en.html) describes the kiosk shell and `--idle-time=0`. Disable monitor hardware sleep as well. TH-08 must later own compositor readiness, VT/PAM session and recovery ordering before enabling boot startup.

For either route, use synthetic text only for graphics diagnostics (`QSG_INFO=1` if needed), record the reported GL renderer and physical mode, confirm local fonts/SVGs/QR and type at 1280 × 720. A llvmpipe/software renderer is not accepted just because an image appears. Do not leave verbose Qt input logging or screenshots containing visitor text enabled in exhibition use. No graphics route has passed this procedure yet.

## Bluetooth keyboard, layout and offline operation

Pair **interactively** during maintenance with the keyboard in its manufacturer's pairing mode. BlueZ's system daemon stores the bond; the kiosk app never pairs a keyboard. Keep a recovery console available. On the Pi:

```sh
sudo systemctl enable --now bluetooth.service
sudo rfkill unblock bluetooth
bluetoothctl
```

Inside `bluetoothctl`, use `power on`, `agent KeyboardDisplay`, `default-agent`, then `scan on`. Identify the **actual keyboard reported by the scan**; never paste a sample MAC address. Type `pair` followed by that actual device identifier, and complete the displayed passkey/confirmation using the real keyboard as directed. Then type `trust`, `connect` and `info`, each followed by that same identifier, and confirm paired/trusted/connected status. Finish with `scan off`, `discoverable off`, then `quit`. If authorization is denied, use the maintenance administrator for pairing, not a root kiosk app. Do not blindly re-run `pair` on an existing bond: current BlueZ may remove an existing pairing first. Use `connect` for reconnection and `remove` only when intentionally repairing a broken bond. See the [official BlueZ command reference](https://manpages.debian.org/trixie/bluez/bluetoothctl.1.en.html).

Configure the actual console keyboard using `sudo dpkg-reconfigure keyboard-configuration` and apply/reboot during maintenance. The console layout is **not** proof of the Qt layout. Wayland uses Weston's `[keyboard] keymap_layout`/variant. EGLFS/libinput uses Qt's XKB input support; record the required `XKB_DEFAULT_LAYOUT`/variant for the installed build and validate punctuation, uppercase, backspace, ENTER and language-specific characters in the app. See [Qt embedded input handling](https://doc.qt.io/qt-6.8/inputs-linux-device.html). Do not disable input or keyboard sleep globally to disguise reconnect failure.

Acceptance still required on the real keyboard: type in the app, let the keyboard sleep naturally, wake it and type again; power-cycle the keyboard; reboot the Pi; start the app with keyboard absent, then connect it. Record wake/reconnect latency, keyboard make/model and layout. The missing keyboard must not crash or block application startup. Do not collect an input-event trace during visitor use.

After installation and pairing, disable **Wi-Fi only**, from the local recovery console:

```sh
sudo rfkill block wifi
rfkill list
```

On an image managed by NetworkManager, `sudo nmcli radio wifi off` is an alternative Wi-Fi-only control; do not assume `nmcli` is installed. Never use `rfkill block all`, `rfkill unblock all`, `dtoverlay=disable-bt` or a Bluetooth service stop. Confirm Bluetooth remains unblocked and connected and repeat the app/keyboard trial with no network, including after reboot. Record persistence of the chosen Wi-Fi policy rather than assuming it. Re-enable Wi-Fi only during maintenance with `sudo rfkill unblock wifi` (or the corresponding NetworkManager setting).

External dependencies are needed to obtain the OS/packages/project and during maintenance, **not for the exhibition interaction**: local fonts, images, JSON content and Segno QR generation stay offline; no AI/API/web server is involved. A visitor's phone needs connectivity to open `https://zwei.berlin/app-repo`. The owner-provided redirect is **not configured yet**, so URL destination/phone acceptance remains blocked even if the local QR renders.

## Sensor electrical gate and unresolved pin map

With each JO-GL534 **disconnected from the Pi and all supplies**, a competent operator must verify passive two-wire continuity, isolation and wet/dry behavior using suitable measurement equipment. Supplied switch voltage/current ratings do not authorize applying those voltages to a GPIO. Keep water and exposed powered electronics separated. Never attach an active sensor output or 5 V to a Pi input.

Only after that verification: power down; document five distinct BCM inputs and their corresponding physical header pins, S1 lowest → S5 highest, avoiding pins reserved by enabled interfaces; wire **3.3 V → passive switch → GPIO input**, with GPIO Zero `pull_up=False`. Record dry/wet raw values per switch and mounting heights before setting `wet_values`. The [GPIO Zero input guide](https://gpiozero.readthedocs.io/en/stable/api_input.html#button) and [lgpio pin factory documentation](https://gpiozero.readthedocs.io/en/stable/api_pins.html#lgpio) describe the intended software backend; lgpio character-device permissions still need physical verification.

The package candidate is **lgpio**, but `sensors.pin_factory` must remain null until it is confirmed on this device. No remote pigpio daemon or automatic backend fallback is part of this baseline. No random pin-driving, GPIO loopback, `gpioset`, pin factory construction or probing is performed by preflight. `hardware_verified=true` may be recorded only after passive-contact safety, the actual BCM/header mapping, backend access and polarity have been verified by the operator. The complete calibration must also exercise all six contiguous levels and invalid patterns. TH-10 owns that physical evidence; the live adapter must not silently choose mock mode on error. Broken/stuck wires can still resemble valid dry/wet readings, so software does not certify circuit safety.

## TH-08 handoff contract (no service installed by TH-02)

- Application identity **`thirsty`**, non-root, no sudo; application working directory **`/opt/thirsty`**; interpreter **`/usr/bin/python3`**; complete source/assets and JSON installed by the operator, not downloaded at boot. TH-08 owns account/home creation and least-privilege device/seat policy.
- App command: `/usr/bin/python3 -m app.main --mode live --device /opt/thirsty/config/device.json --script /opt/thirsty/config/script.json --fullscreen`. Before the electrical/config gate, manual validation uses **explicit `--mode mock`**; never automatic mock fallback and never boot live with unknown pins.
- Deployment tooling selection: `--display-backend eglfs|wayland`; this is **not an app argument**. App sensor selection is `--mode mock|live`. No installer mode is inferred from environment. Qt's `QT_QPA_PLATFORM` is set explicitly by the selected display lifecycle.
- EGLFS contract: `QT_QPA_PLATFORM=eglfs`, `QT_QPA_EGLFS_INTEGRATION=eglfs_kms`, `QT_QPA_EGLFS_KMS_CONFIG=/etc/thirsty/eglfs.json`, `QSG_RHI_BACKEND=opengl`; no compositor, owned active VT, verified DRM/input access. Only usable if actual package and hardware gates pass.
- Wayland contract: packaged Weston DRM/GL kiosk shell, idle disabled, owned active VT/logind session; socket **`thirsty-wayland`** in the private same-user runtime directory; app gets `QT_QPA_PLATFORM=wayland`, `WAYLAND_DISPLAY=thirsty-wayland`, `QSG_RHI_BACKEND=opengl`. TH-08 must provide readiness and restart ordering. Do not run both routes or silently substitute one.
- Hardware-backed final choice is **unresolved**. Package-supported Wayland is an explicit candidate, not a measured decision. Do not enable a boot unit until TH-02 physical evidence selects one route and TH-08 verifies that route as the dedicated identity. Keep logs bounded/volatile and free of visitor text. This document creates no service files or boot configuration.

## Operator-filled installation record and outstanding acceptance

Leave unknown values empty/null in the device record, not guessed. Store the actual dated record and preflight evidence privately alongside the installation documentation; no physical values are supplied here.

| Field                                                                            | Current evidence / required operator entry                                         |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Official OS image URL, filename, release date                                    | Not recorded — Pi unavailable                                                      |
| Published SHA-256, locally computed SHA-256, verification date/tool              | Not recorded — do not substitute a hash of a different image                       |
| Flash verification, card make/capacity, project revision                         | Not recorded                                                                       |
| Pi model / RAM / userspace / kernel observed                                     | Not measured; required Pi 3 A+, 512 MB, armhf                                      |
| Apt origins/candidate plan; installed package versions                           | Target not installed; attach reviewed plan and preflight JSON                      |
| Chosen graphics route, Qt plugin paths, renderer, DRM connector/mode             | Unresolved; record actual 1280 × 720 scanout and GPU renderer                      |
| Dedicated identity, seat/VT, runtime directory, device permissions               | Awaiting TH-08 and physical verification                                           |
| Screen model, monitor sleep setting, blanking trial duration                     | Not recorded                                                                       |
| Keyboard model/layout, pairing, reboot and sleep/wake reconnect                  | Not tested; record results and latency, omit address from public evidence          |
| Supply rating, measured power behavior, HDMI/screen power arrangement            | Not measured; record `get_throttled`, temperature and any voltage-warning evidence |
| BCM/header mapping S1–S5, passive-contact evidence, wet/dry values, lgpio access | All unknown/unverified; keep hardware config null/false                            |
| Wi-Fi off/Bluetooth on; offline startup and typing after reboot                  | Not tested                                                                         |
| Idle, active typing, scrolling and completion memory/swap                        | Not measured; collect process RSS/high-water/swap plus system free/swap over time  |
| Long-run no OOM, no sustained swapping, stable responsiveness                    | Not tested; inventory alone is insufficient on 512 MB                              |
| Final URL redirect and phone QR scan from HDMI                                   | Owner redirect unconfigured; physical scan not tested                              |

For memory acceptance, take separate preflight records with the actual app PID at stable Start, while typing synthetic text, during long transcript scrolling and after reset; repeat over time and include the compositor's PID separately for Wayland. `free`/`vmstat`/`swapon` are snapshots, not proof of no sustained swapping. Observe responsiveness and consult kernel OOM/power diagnostics during maintenance without collecting visitor session text. `vcgencmd get_throttled` contains current and historical flags; use [Raspberry Pi's documented meanings](https://www.raspberrypi.com/documentation/computers/os.html#vcgencmd) and do not clear/reboot away evidence before recording it. Persistent throttling, OOM, sustained swapping, missing plugins, wrong layout, blanking or reconnect failure block deployment rather than being hidden with larger swap or a silent graphics fallback.
