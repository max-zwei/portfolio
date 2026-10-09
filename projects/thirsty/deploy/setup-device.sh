#!/bin/bash
# Operator-invoked package setup only. No GPIO, boot config, services or users changed here.
set -euo pipefail
export LC_ALL=C

usage() {
    cat <<'USAGE'
Usage: bash deploy/setup-device.sh --display-backend eglfs|wayland [--apply]

Default: inspect the local apt cache, print candidates, simulate installation.
--apply: require root and perform that exact candidate-version package install.
Run sudo apt-get update separately on the Pi before planning. No pip, OS upgrade,
repository addition, automatic backend fallback, service installation, reboot,
user creation, radio change, modesetting or GPIO access is performed here.
EGLFS is only a requested route: it is NOT supplied by stock Debian Trixie Qt.
The installed Pi Qt must expose EGLFS/KMS before that route can be used.
USAGE
}

fail() { printf '%s\n' "$*" >&2; exit 2; }
backend=''
apply=0
while (($#)); do
    case "$1" in
        --help|-h) usage; exit 0 ;;
        --display-backend)
            (($# >= 2)) || fail 'Missing --display-backend value'
            backend=$2; shift 2 ;;
        --apply) apply=1; shift ;;
        *) fail "Unknown argument: $1" ;;
    esac
done
case "$backend" in eglfs|wayland) ;; *) usage; fail 'Select exactly one supported display backend explicitly.' ;; esac
if ((apply)) && ((EUID != 0)); then
    fail '--apply requires explicit sudo invocation on the target Pi.'
fi
for program in python3 apt-cache apt-get dpkg; do
    command -v "$program" >/dev/null || fail "Required command unavailable: $program"
done
script_dir=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
# This is passive inventory, not a hardware/graphics acceptance test. A 64-bit
# kernel is allowed when dpkg and the actual Python userspace are 32-bit armhf.
/usr/bin/python3 "$script_dir/preflight.py" --require-pi >/dev/null ||
    fail 'Target guard failed. Run preflight.py for the model/OS/architecture evidence.'

packages=()
while IFS= read -r package || [[ -n "$package" ]]; do
    [[ -z "$package" || "$package" == \#* ]] && continue
    [[ "$package" =~ ^[a-z0-9][a-z0-9+.-]+$ ]] || fail "Invalid package manifest entry: $package"
    packages+=("$package")
done < "$script_dir/packages.txt"
if [[ "$backend" == wayland ]]; then
    packages+=(qt6-wayland weston)
fi

specs=()
for package in "${packages[@]}"; do
    candidate=''
    policy=$(apt-cache policy "$package")
    while read -r key value rest; do
        if [[ "$key" == 'Candidate:' ]]; then candidate=$value; fi
    done <<< "$policy"
    [[ -n "$candidate" && "$candidate" != '(none)' ]] ||
        fail "No apt candidate for $package. Check official Trixie/Pi repositories and apt-get update; no fallback is permitted."
    minimum=''
    maximum=''
    case "$package" in
        python3) minimum='3.11'; maximum='4' ;;
        python3-pyside6.*) minimum='6.8'; maximum='7' ;;
        python3-gpiozero) minimum='2'; maximum='3' ;;
        python3-segno) minimum='1.6'; maximum='2' ;;
        python3-lgpio) minimum='0.2.2' ;;
    esac
    if [[ -n "$minimum" ]]; then
        dpkg --compare-versions "$candidate" ge "$minimum" ||
            fail "$package candidate $candidate is older than supported $minimum. Do not mix Debian releases or install pip wheels."
    fi
    if [[ -n "$maximum" ]]; then
        dpkg --compare-versions "$candidate" lt "$maximum" ||
            fail "$package candidate $candidate is outside the supported major version range (<$maximum)."
    fi
    printf '%s=%s\n' "$package" "$candidate"
    specs+=("$package=$candidate")
done

printf '\nRequested backend: %s. Simulating version-selected apt transaction.\n' "$backend"
apt-get --simulate --no-install-recommends --no-remove install "${specs[@]}"
if ((apply)); then
    # Keep apt's own confirmation prompt: never unattended or --allow-unauthenticated.
    apt-get --no-install-recommends --no-remove install "${specs[@]}"
    printf '\nPackages installed. This does NOT certify hardware or start the application.\n'
    printf 'Run as the eventual non-root kiosk identity: /usr/bin/python3 %q --display-backend %q --require-pi --require-software\n' "$script_dir/preflight.py" "$backend"
else
    printf '\nPlan only: no packages installed. Review candidates and disk use, then explicitly invoke with sudo and --apply.\n'
fi
