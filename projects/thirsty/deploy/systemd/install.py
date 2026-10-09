#!/usr/bin/env python3
"""Operator-only installation. Default is a portable, side-effect-free plan."""
import sys
sys.dont_write_bytecode = True
import argparse
import grp
from itertools import chain
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess

from gate import APP, ETC, require, validate

SOURCE = Path(__file__).resolve().parent


def command(*args):
    subprocess.run(args, check=True)


def install(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    shutil.copyfile(source, destination)
    os.chown(destination, 0, 0)
    destination.chmod(0o644)


def require_immutable_app():
    # Validate ancestors first: a writable parent can replace a protected checkout.
    # lstat rejects symlinks without following them, including ancestor symlinks.
    for path in chain(reversed(APP.parents), (APP,), APP.rglob('*')):
        info = path.lstat()
        require(not path.is_symlink(), f'Symlinks not accepted in installed app path: {path}')
        require(info.st_uid == 0 and not info.st_mode & 0o022,
                f'App and ancestors must be root-owned, not group/world writable: {path}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--display-backend', choices=('eglfs', 'wayland'), required=True)
    parser.add_argument('--mode', choices=('live', 'mock'), required=True)
    parser.add_argument('--approval', type=Path, required=True, help='Private operator physical approval JSON')
    parser.add_argument('--display-config', type=Path, required=True, help='Approved eglfs.json or weston.ini')
    parser.add_argument('--apply', action='store_true', help='Root-only target installation, never starts service')
    parser.add_argument('--enable', action='store_true', help='With --apply only: enable next boot, never start now')
    args = parser.parse_args()
    require(not args.enable or args.apply, '--enable requires --apply')
    if not args.apply:
        print(f'PLAN ONLY: {args.display_backend}, explicitly {args.mode}; no files or host state changed.')
        print('Apply will gate Pi/software, physical display approval, app config and permissions;')
        print('create dedicated thirsty identity, install one PAM/VT7 service and private journal namespace.')
        print('No packages, radio changes, boot config edits, starts or automatic fallback.')
        print(f'Approval: {args.approval}; display config: {args.display_config}; app: {APP}')
        return
    require(sys.platform == 'linux' and os.geteuid() == 0, '--apply requires root on the selected Pi')
    # Serialize operator writes, not app sessions. No lock/file created in dry-run.
    import fcntl
    with open('/run/lock/thirsty-install.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        require_immutable_app()
        validate(args.approval, args.display_backend, args.mode, args.display_config)
        for program in ('systemctl', 'useradd', 'usermod', 'runuser', 'chvt', 'setterm'):
            require(shutil.which(program), f'Missing prerequisite: {program}')
        command('dpkg-query', '-W', '-f=${Status}\n', 'libpam-systemd')
        require(any(Path('/usr/lib').glob('*/security/pam_systemd.so')), 'libpam-systemd PAM module required')
        for group in ('video', 'render', 'input', 'gpio'):
            grp.getgrnam(group)  # Existing image udev groups only, never invented device rules.
        require(subprocess.run(['systemctl', 'is-active', '--quiet', 'thirsty.service']).returncode != 0,
                'Stop thirsty.service explicitly before installing or changing routes')
        require(subprocess.run(['systemctl', 'is-active', '--quiet', 'display-manager.service']).returncode != 0,
                'A competing display manager owns the seat; resolve explicitly before installation')
        try:
            account = pwd.getpwnam('thirsty')
            require(account.pw_uid != 0 and account.pw_dir == '/var/lib/thirsty' and
                    account.pw_shell == '/usr/sbin/nologin', 'Existing thirsty identity is not dedicated')
            require(grp.getgrgid(account.pw_gid).gr_name == 'thirsty', 'Existing identity needs private primary group')
        except KeyError:
            command('useradd', '--system', '--user-group', '--create-home', '--home-dir',
                    '/var/lib/thirsty', '--shell', '/usr/sbin/nologin', 'thirsty')
        groups = 'video,render,input' + (',gpio' if args.mode == 'live' else '')
        # Exact groups, not -a: no inherited sudo or stale live GPIO access in mock mode.
        command('usermod', '--groups', groups, '--lock', 'thirsty')
        # A later write/readability failure must not leave an old enabled boot path.
        if Path('/etc/systemd/system/thirsty.service').exists():
            command('systemctl', 'disable', 'thirsty.service')
        install(args.approval, ETC / 'approval.json')
        display_name = 'eglfs.json' if args.display_backend == 'eglfs' else 'weston.ini'
        install(args.display_config, ETC / display_name)
        selection = ETC / 'selection.json'
        selection.write_text(json.dumps({'backend': args.display_backend, 'mode': args.mode}) + '\n')
        os.chown(selection, 0, 0)
        selection.chmod(0o644)
        for name in ('run.py', 'gate.py'):
            install(SOURCE / name, '/usr/local/lib/thirsty/' + name)
        install(SOURCE / 'thirsty.pam', '/etc/pam.d/thirsty')
        install(SOURCE / 'thirsty.service', '/etc/systemd/system/thirsty.service')
        install(SOURCE / 'journald-thirsty.conf', '/etc/systemd/journald@thirsty.conf.d/limits.conf')
        install(SOURCE / 'journal-volatile.conf', '/etc/systemd/system/systemd-journald@thirsty.service.d/volatile.conf')
        # Readability and schema gates as actual unprivileged identity; still no GPIO opens.
        command('runuser', '-u', 'thirsty', '--', '/usr/bin/python3', '-c',
                'import sys; sys.path.insert(0,"/usr/local/lib/thirsty"); '
                'from gate import validate; validate(*sys.argv[1:])',
                str(ETC / 'approval.json'), args.display_backend, args.mode, str(ETC / display_name))
        command('systemctl', 'daemon-reload')
        # Applying without --enable also clears any previous boot enablement.
        command('systemctl', 'enable' if args.enable else 'disable', 'thirsty.service')
        print('Installed; not started. Boot enablement: ' + ('enabled' if args.enable else 'disabled'))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f'Installation refused: {exc}', file=sys.stderr)
        sys.exit(2)
