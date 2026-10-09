"""One seat/session; compositor failure always discards the application session."""
import ctypes
import ctypes.util
import fcntl
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import threading
import time

from gate import APP, ETC, require, validate


def probe():
    lib = ctypes.CDLL(ctypes.util.find_library('wayland-client') or 'libwayland-client.so.0')
    lib.wl_display_connect.argtypes = [ctypes.c_char_p]
    lib.wl_display_connect.restype = ctypes.c_void_p
    lib.wl_display_roundtrip.argtypes = [ctypes.c_void_p]
    lib.wl_display_roundtrip.restype = ctypes.c_int
    lib.wl_display_disconnect.argtypes = [ctypes.c_void_p]
    display = lib.wl_display_connect(b'thirsty-wayland')
    if not display:
        return 1
    try:
        return 0 if lib.wl_display_roundtrip(display) >= 0 else 1
    finally:
        lib.wl_display_disconnect(display)


def exec_child(parent_pid, argv):
    """Arm parent-death protection before exec; reject death during fork/setup."""
    libc = ctypes.CDLL(None, use_errno=True)
    libc.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong,
                           ctypes.c_ulong, ctypes.c_ulong]
    libc.prctl.restype = ctypes.c_int
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    # Checking only before prctl would leave a parent-death race.
    if os.getppid() != parent_pid:
        os.kill(os.getpid(), signal.SIGKILL)
        os._exit(1)
    os.execvpe(argv[0], argv, os.environ)


def spawn(argv, **kwargs):
    # A fresh interpreter avoids Python preexec_fn in a potentially threaded parent.
    return subprocess.Popen(['/usr/bin/python3', __file__, '--child',
                             str(os.getpid()), *argv], **kwargs)


def main():
    require(os.getuid() != 0, 'Never run kiosk as root')
    selection = json.loads((ETC / 'selection.json').read_text())
    backend, mode = selection['backend'], selection['mode']
    display = ETC / ('eglfs.json' if backend == 'eglfs' else 'weston.ini')
    record = validate(ETC / 'approval.json', backend, mode, display)
    runtime = Path('/run/thirsty')
    info = runtime.stat()
    require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o700, 'Runtime must be private and owned by thirsty')
    lock = (runtime / 'seat.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    env = os.environ.copy()
    for key in ('DISPLAY', 'WAYLAND_DISPLAY', 'QT_QPA_EGLFS_INTEGRATION',
                'QT_QPA_EGLFS_KMS_CONFIG', 'QT_QUICK_BACKEND', 'QT_QPA_ENABLE_TERMINAL_KEYBOARD'):
        env.pop(key, None)
    env.update(XDG_RUNTIME_DIR=str(runtime), LG_WD=str(runtime), QSG_RHI_BACKEND='opengl',
               QT_QPA_PLATFORM=backend, XKB_DEFAULT_LAYOUT=record['keyboard_layout'])
    # This is the service's actual owned VT, not an SSH pseudo-terminal.
    subprocess.run(['/usr/bin/setterm', '--blank', '0', '--powersave', 'off', '--powerdown', '0'],
                   check=True, env={**env, 'TERM': 'linux'}, stdout=sys.stdin)
    stopping = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stopping.set())
    children = []
    try:
        if backend == 'wayland':
            env['WAYLAND_DISPLAY'] = 'thirsty-wayland'
            weston = spawn(['/usr/bin/weston', '--backend=drm', '--renderer=gl',
                '--shell=kiosk-shell.so', '--idle-time=0', '--socket=thirsty-wayland',
                '--drm-device=' + Path(record['drm_card']).name, '--config=' + str(display)], env=env)
            children.append(weston)
            deadline = time.monotonic() + 20
            ready = False
            while not stopping.is_set() and weston.poll() is None and time.monotonic() < deadline:
                path = runtime / 'thirsty-wayland'
                if path.exists() and stat.S_ISSOCK(path.stat().st_mode):
                    try:
                        result = subprocess.run(['/usr/bin/python3', __file__, '--probe'], env=env,
                                                timeout=min(2, max(0.01, deadline-time.monotonic())),
                                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if result.returncode == 0:
                            ready = True
                            break
                    except subprocess.TimeoutExpired:
                        pass
                stopping.wait(0.1)
            if stopping.is_set():
                return 0
            require(ready, 'Weston protocol readiness deadline exceeded or compositor exited')
        else:
            env.update(QT_QPA_EGLFS_INTEGRATION='eglfs_kms', QT_QPA_EGLFS_KMS_CONFIG=str(display))
        children.append(spawn(['/usr/bin/python3', '-m', 'app', '--mode', mode,
            '--device', str(APP / 'config/device.json'), '--script', str(APP / 'config/script.json'),
            '--fullscreen'], cwd=APP, env=env))
        while not stopping.wait(0.1):
            if any(child.poll() is not None for child in children):
                # Even an unexpected clean exit restarts both into a fresh Start.
                return 1
        return 0
    finally:
        # App first, while the compositor is still alive, for Qt/GPIO cleanup.
        for child in reversed(children):
            if child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
        lock.close()


if __name__ == '__main__':
    try:
        if sys.argv[1:2] == ['--child']:
            exec_child(int(sys.argv[2]), sys.argv[3:])
        else:
            sys.exit(probe() if sys.argv[1:] == ['--probe'] else main())
    except Exception as exc:
        # Only deployment failures, never visitor text or child environments.
        print(f'thirsty lifecycle: {type(exc).__name__}: {exc}', file=sys.stderr)
        sys.exit(1)
