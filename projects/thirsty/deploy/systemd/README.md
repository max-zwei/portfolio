# TH-08: explicit native kiosk boot lifecycle

These files implement the reachable deployment procedure, **not physical acceptance**. No Pi is available; systemd/PAM/DRM/VT boot, signal/GPIO cleanup, GPU scanout and Bluetooth reconnect remain untested. The final graphics route is unresolved. Use official Raspberry Pi OS Lite **Trixie armhf**, system Python, and the common manifest/package procedure in `../packages.txt`, `../setup-device.sh` and `../../docs/device.md`. Bookworm uses similar logind/PAM concepts but is not accepted by this baseline's target gate.

Stock documented Trixie Qt packages do not supply EGLFS/KMS. Do not enable that route unless the actual installed official build has **both** plugins and passes physical rendering acceptance. Wayland requires explicitly installing `qt6-wayland weston` through TH-02. There is no fallback, custom Qt build, pip wheel, browser, server or software renderer. Commands here use the public entry point **`python3 -m app`**, superseding older `app.main` examples in the baseline documentation.

## Files and architecture

One `thirsty.service` owns reserved **VT7 / seat0**, with a dedicated PAM/logind session and non-root `thirsty` identity. `chvt 7` is the only privileged service pre-command; app and Weston never run as root. `PAMName=thirsty` requires installed `libpam-systemd` and `/etc/pam.d/thirsty`; failed session setup must fail, not silently bypass logind. VT7 getty conflicts with the service. Do not run another compositor, desktop, automatic login or keyboard reader on this seat. Keep a separate maintenance console, normally VT1, and an operator keyboard before starting.

`run.py` is a small lifecycle supervisor, not another experience process. EGLFS runs only Qt; Wayland runs Weston DRM/GL kiosk shell and then the same Qt command:

```
/usr/bin/python3 -m app --mode live --device /opt/thirsty/config/device.json --script /opt/thirsty/config/script.json --fullscreen
```

The sensor argument is `mock` **only when the operator explicitly selects `--mode mock`**. Mock is a display/recovery trial, not a live installation. Live additionally gates five distinct BCM pins, matching physical header pins, `hardware_verified=true` and verified `lgpio`. Approval is an operator assertion, not an electrical safety test. Complete the passive-contact and polarity procedure before authorizing live.

The runtime directory `/run/thirsty` is systemd-created mode 0700, owned by the same user as both processes. `LG_WD` points lgpio's notification files there, never into the immutable app checkout. A nonblocking `flock` protects the seat lifecycle. Weston uses private socket `thirsty-wayland`; Qt starts only after a bounded 20-second readiness window with an actual libwayland-client connection and protocol roundtrip. Each probe has its own deadline. No fixed startup sleep is used. A compositor **or** application exit tears down the other process and fails the service, so `Restart=on-failure` produces a fresh app Start with no restored transcript. Four starts in 120 seconds and five-second restart spacing bound failures. Manual `systemctl stop` is not restarted. SIGTERM is forwarded to the application first, allowing its integrated GPIO cleanup, then Weston; each gets eight seconds before forced termination.

Both direct long-lived children enter through a fresh Python wrapper that arms Linux `PR_SET_PDEATHSIG=SIGKILL`, then checks the expected supervisor PID before exec. This closes the fork/setup parent-death race and kills the app and Weston if the supervisor is killed, even after PAM/logind moves them outside the service cgroup. Do not rely on `KillMode=mixed` to clean up that session scope. Forced SIGKILL cannot run Python/GPIO cleanup; kernel device release and a fresh restart still need target verification. The contract covers the directly executed non-setuid app/compositor, not arbitrary daemonizing grandchildren.

## Prerequisites and approval record

1. Complete TH-02 package installation and target/software preflight. This helper does not install packages, rewrite repositories, configure KMS firmware or modify radios. Confirm `libpam-systemd` is installed (normal Lite prerequisite); inspect image udev groups `video`, `render`, `input`, `gpio` and their actual device-node ownership. Never create replacement permissive udev rules or use `chmod 666`. No `PrivateDevices` sandbox is used because it would hide required devices.
2. Install a reviewed, complete source/assets/config tree at `/opt/thirsty`, **root-owned and without group/world write permissions or symlinks**. Do not copy `.venv`, mutable caches or generated app files. `output/app` must remain empty. The helper does not copy the checkout. Sensor and script configuration must parse through the actual app loaders. Keep `/opt`, `/etc/thirsty`, `/usr/local/lib/thirsty` and their parent directories root-controlled.
3. Trial the selected route in a real active local login session following `docs/device.md`, first with mock inputs. Repeat under the dedicated identity before approving permissions. If a temporary interactive `thirsty` account is needed for that physical trial, the operator may create it with home `/var/lib/thirsty`, private primary group and only the required device groups; afterward set shell `/usr/sbin/nologin` and lock its password. Do not leave an interactive password, sudo authorization or another login process on the seat. The installer normally creates this account itself; it rejects an existing non-dedicated account.
4. Record observed DRM card, **backend-reported connector name**, keyboard layout, GL renderer, actual 1280×720 mode, active seat and node permissions in a private dated installation record. Confirm monitor sleep disabled and console blanking suppressed. The service applies `setterm --blank 0 --powersave off --powerdown 0` on its actual VT and fails if unsupported; resolve the device blanking policy rather than hiding the error. No boot cmdline is edited automatically.
5. Supply a private approval JSON with these fields, populated from that record (no device/card/connector values are supplied by this repository):
   - `backend`: exactly `eglfs` or `wayland`;
   - `drm_card`: observed `/dev/dri/card` device path with numeric suffix;
   - `connector`: exact Qt or Weston connector, respectively;
   - `keyboard_layout`: actual XKB layout (for example, a layout list is permitted);
   - `record`: nonempty reference to dated private evidence;
   - `graphics_verified`, `seat_verified`, `permissions_verified`, `blanking_verified`: booleans, all true only after physical verification.
6. Supply one reviewed display config. EGLFS JSON requires `device` matching the approved card and exactly one `outputs` entry with approved `name` and `mode: "1280x720"`. Other disconnected/unused connectors must not contend for output; physically validate the resulting scanout. Weston INI requires `[core]` `shell=kiosk-shell.so`, `idle-time=0`, `xwayland=false`, `require-input=false`; `[output]` approved `name`, `mode=1280x720`, `scale=1`; `[keyboard]` `keymap_layout` matching approval. `require-input=false` permits boot without a connected keyboard rather than exhausting restarts before Bluetooth reconnects. Additional keyboard variant options may be specified in Weston INI. For EGLFS this helper supports the approved layout only; verify actual punctuation and language-specific input. Weston command-line options explicitly select DRM, GL, kiosk shell, socket and approved card; no headless/nested backend.

The app does not need network access. `RestrictAddressFamilies=AF_UNIX AF_NETLINK` permits local Wayland/logind sockets and the compositor's required udev device/hotplug monitors; AF_INET and AF_INET6 remain denied. Bluetooth HID arrives through local evdev, not app Bluetooth connections. Assets/configs and home are read-only under the service; only volatile runtime/private temporary files are writable. Python bytecode, QML disk and Mesa shader caches are disabled. QR SVG handoff uses the app's data URL; there are no app cookies or generated handoff files to persist. Device group membership is exact, not additive: `video,render,input` plus `gpio` **only in live mode**. Group membership alone is not DRM master permission: PAM/logind, active VT, no seat competitor and actual device ownership must all be validated.

## Safe planning and explicit install

From the checkout, both commands below are safe on a workstation and do not access hardware or change host state. Paths may be planned before the corresponding private files exist:

```sh
python3 deploy/systemd/install.py --help
python3 deploy/systemd/install.py --display-backend wayland --mode mock \
  --approval /private/operator/approval.json --display-config /private/operator/weston.ini
```

On the selected Pi only, after approval and checkout preparation:

```sh
sudo /usr/bin/python3 deploy/systemd/install.py --display-backend wayland --mode mock \
  --approval /private/operator/approval.json --display-config /private/operator/weston.ini --apply
```

Run the installer from a trusted root-controlled checkout. Before importing installed app validation code or executing installed preflight, apply rejects symlinks, non-root ownership and group/world write permissions throughout `/opt/thirsty` and its ancestors. It then gates target/software/config, creates or constrains the kiosk account, and installs the unit, helper, dedicated PAM file and **namespace-only** journal configuration. It repeats passive preflight and config checks as `thirsty`. Installation is serialized with `/run/lock/thirsty-install.lock`. Existing service must be explicitly stopped first. Applying without `--enable` leaves it disabled, including a previously enabled installation. It never starts the kiosk, starts a display manager, masks gettys, pairs keyboards or reboots. Failures are not transactional: inspect installed files before retrying; boot enablement is withheld on failed updates after the disable step.

Use `--display-backend eglfs --display-config /private/operator/eglfs.json` only for that physically approved route. Use `--mode live` only after the live gate passes. Repeat the entire explicit installer selection when changing route/mode; never edit only an environment variable to bypass gates. A selected route/config failure never substitutes the other route or mock sensors.

First start is operator-controlled:

```sh
sudo systemctl start thirsty.service
systemctl status thirsty.service
journalctl --namespace=thirsty -u thirsty.service --since today
loginctl session-status
sudo systemctl stop thirsty.service
sudo systemctl restart thirsty.service
```

Inspect the service's actual session with `loginctl` (active seat0, VT7 and correct user), permissions and actual hardware mode. Validate synthetic typing, prolonged idle, app and compositor kill recovery into Start, manual stop, GPIO cleanup, no competing getty, start-limit behavior and reboot. `systemctl reset-failed thirsty.service` clears the rate limit **only after fixing the cause**. Do not log visitor text, input traces, environments or screenshots; keep Qt verbose diagnostics off in visitor operation.

Only after these trials authorize boot by repeating the full selected installer command with **both `--apply --enable`**. It still does not start immediately. This is the only helper path that enables boot. Preflight is repeated at each service invocation, so later invalid configs, missing plugins or changed packages fail closed. Inventory flags never replace physical evidence.

## Journal and keyboard lifecycle

`LogNamespace=thirsty` routes stdout/stderr to a dedicated journal. Namespace configuration uses volatile storage, 16 MiB cap, 4 MiB files, 32 MiB free-space reserve, one-day retention and rate limits. The instance-only service drop-in clears `LogsDirectory`; the global journald policy is untouched. If updating this policy while its namespace daemon is already running, stop the kiosk, then explicitly restart `systemd-journald@thirsty.service` before the next trial. Inspect namespace retention and RAM pressure on the actual 512 MB device. No host journal changes or journal fixtures are applied on a workstation.

`Wants=`/`After=bluetooth.service` orders the kiosk after an optional BlueZ startup attempt, but does not require a successful daemon or connected keyboard. There is no device-address dependency or keyboard wait loop. Pair/trust the real keyboard interactively during maintenance using the baseline procedure; verify wake, reconnect, absent-at-boot then connect, keyboard power cycle and Pi reboot. Keep Bluetooth enabled/unblocked. Disable **Wi-Fi only** using `rfkill block wifi` (or the image's Wi-Fi-specific NetworkManager policy); never block all radios or disable Bluetooth. Check persistence and offline typing after reboot. The installer deliberately does not alter radio or pairing state. The QR redirect is still owner-unconfigured and cannot be accepted by service setup.

## Stop and rollback

Keep maintenance access and a backup of pre-existing operator files. Stop and disable first:

```sh
sudo systemctl disable --now thirsty.service
sudo systemctl stop systemd-journald@thirsty.service systemd-journald@thirsty.socket
sudo rm /etc/systemd/system/thirsty.service /etc/pam.d/thirsty
sudo rm /etc/systemd/journald@thirsty.conf.d/limits.conf
sudo rm /etc/systemd/system/systemd-journald@thirsty.service.d/volatile.conf
sudo systemctl daemon-reload
sudo chvt 1
```

Restore backed-up files instead of deleting paths that predated this installation. These are **operator commands**, never automatic cleanup. The helper does not mask or enable `getty@tty7`; if it was previously active, restore its recorded prior state explicitly after stopping the kiosk. Keep `/opt/thirsty`, `/etc/thirsty`, installed helpers, user/home and Bluetooth bonds for diagnosis; remove only these known kiosk-owned resources separately after reviewing ownership and backups. Do not remove common packages or alter global journald/radio policy as rollback. A mock-to-live or backend change needs fresh physical approval, then explicit reinstall; no automatic recovery route exists.

## Pending validation

No target checks are claimed here. Parent verification should cover Python syntax, portable `--help`/plan, refused workstation apply, gate fixtures (including immutable ancestors, invalid live pins/approval/config and absent `require-input=false`), parent-death setup/failure/race ordering, and bounded Wayland protocol timeout/child teardown. A Linux systemd host must check unit/PAM/journal parsing and actual supervisor SIGKILL with no surviving app/compositor. The actual Pi must prove VT/logind access, netlink/udev startup and input hotplug, lgpio notification creation under `/run/thirsty`, GL mode, idle blanking, restart/start-limit/manual-stop semantics, resource limits, GPIO release after forced death and keyboard-absent boot followed by reconnect. No boot, hardware or Bluetooth test has been performed.
