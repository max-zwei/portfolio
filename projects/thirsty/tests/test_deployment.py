"""Portable deployment regressions; no GPIO, compositor or systemd is started."""
import importlib.util
from pathlib import Path
import signal
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def deployment(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / 'deploy/systemd'))
    modules = {}
    for name in ('run', 'install'):
        spec = importlib.util.spec_from_file_location(
            'deployment_' + name, ROOT / 'deploy/systemd' / (name + '.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[name] = module
    return SimpleNamespace(**modules)


@pytest.mark.parametrize('parent_alive', [True, False])
def test_parent_death_is_armed_before_identity_check(deployment, monkeypatch, parent_alive):
    run = deployment.run
    events = []
    prctl = Mock(side_effect=lambda *args: events.append(('prctl', args)) or 0)
    monkeypatch.setattr(run.ctypes, 'CDLL', lambda *a, **kw: SimpleNamespace(prctl=prctl))
    monkeypatch.setattr(run.os, 'getppid', lambda: events.append(('parent',)) or (123 if parent_alive else 1))
    monkeypatch.setattr(run.os, 'getpid', lambda: 456)
    monkeypatch.setattr(run.os, 'kill', lambda *args: events.append(('kill', args)))
    monkeypatch.setattr(run.os, '_exit', Mock(side_effect=SystemExit(1)))
    monkeypatch.setattr(run.os, 'execvpe', lambda *args: events.append(('exec', args)))
    if parent_alive:
        run.exec_child(123, ['/bin/target', '--flag'])
        assert events[2][0] == 'exec'
        assert events[2][1][:2] == ('/bin/target', ['/bin/target', '--flag'])
    else:
        with pytest.raises(SystemExit):
            run.exec_child(123, ['/bin/target'])
        assert events[2] == ('kill', (456, signal.SIGKILL))
        assert not any(event[0] == 'exec' for event in events)
    assert events[:2] == [('prctl', (1, signal.SIGKILL, 0, 0, 0)), ('parent',)]


def test_parent_death_setup_failure_never_executes(deployment, monkeypatch):
    run = deployment.run
    monkeypatch.setattr(run.ctypes, 'CDLL', lambda *a, **kw: SimpleNamespace(prctl=Mock(return_value=-1)))
    monkeypatch.setattr(run.ctypes, 'get_errno', lambda: 1)
    execute = Mock()
    monkeypatch.setattr(run.os, 'execvpe', execute)
    with pytest.raises(OSError):
        run.exec_child(123, ['/bin/target'])
    execute.assert_not_called()


@pytest.mark.parametrize('bad_kind', ['owner', 'writable', 'symlink'])
@pytest.mark.parametrize('bad_index', range(4))
def test_immutable_gate_rejects_ancestors_tree_and_links(deployment, monkeypatch, bad_kind, bad_index):
    visited = []

    class Node:
        def __init__(self, index):
            self.index = index

        def lstat(self):
            visited.append(self.index)
            bad = self.index == bad_index
            return SimpleNamespace(st_uid=1000 if bad and bad_kind == 'owner' else 0,
                                   st_mode=0o777 if bad and bad_kind == 'writable' else 0o755)

        def is_symlink(self):
            return self.index == bad_index and bad_kind == 'symlink'

    root, opt, app, child = [Node(i) for i in range(4)]
    app.parents = (opt, root)
    app.rglob = lambda pattern: iter((child,))
    monkeypatch.setattr(deployment.install, 'APP', app)
    with pytest.raises(ValueError):
        deployment.install.require_immutable_app()
    assert visited == list(range(bad_index + 1))


@pytest.mark.parametrize('require_input', [None, 'true', 'false'])
def test_weston_requires_keyboard_independent_startup(deployment, monkeypatch, tmp_path, require_input):
    import gate
    import json
    monkeypatch.setattr(gate, 'APP', ROOT)
    monkeypatch.setattr(Path, 'is_char_device', lambda self: True)
    preflight = Mock()
    monkeypatch.setattr(gate.subprocess, 'run', preflight)
    approval = tmp_path / 'approval.json'
    approval.write_text(json.dumps({
        'backend': 'wayland', 'graphics_verified': True, 'seat_verified': True,
        'permissions_verified': True, 'blanking_verified': True,
        'record': 'synthetic test only', 'connector': 'TEST-1', 'keyboard_layout': 'us',
        'drm_card': '/dev/dri/card0',
    }))
    display = tmp_path / 'weston.ini'
    display.write_text(
        '[core]\nshell=kiosk-shell.so\nidle-time=0\nxwayland=false\n'
        + ('' if require_input is None else f'require-input={require_input}\n')
        + '[output]\nname=TEST-1\nmode=1280x720\nscale=1\n'
        '[keyboard]\nkeymap_layout=us\n')
    if require_input == 'false':
        gate.validate(approval, 'wayland', 'mock', display)
        preflight.assert_called_once()
    else:
        with pytest.raises(ValueError, match=r'core.require-input=false'):
            gate.validate(approval, 'wayland', 'mock', display)
        preflight.assert_not_called()
