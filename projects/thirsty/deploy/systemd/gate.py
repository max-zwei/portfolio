"""Passive deployment gates shared by installer and the non-root service."""
import configparser
import json
import os
from pathlib import Path
import re
import subprocess
import sys

APP = Path('/opt/thirsty')
ETC = Path('/etc/thirsty')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(approval, backend, mode, display):
    require(backend in ('eglfs', 'wayland'), 'Explicit graphics backend required')
    require(mode in ('live', 'mock'), 'Explicit sensor mode required')
    record = json.loads(Path(approval).read_text())
    require(record.get('backend') == backend, 'Approval backend mismatch')
    for key in ('graphics_verified', 'seat_verified', 'permissions_verified', 'blanking_verified'):
        require(record.get(key) is True, f'Operator physical approval required: {key}')
    for key in ('record', 'connector', 'keyboard_layout'):
        require(isinstance(record.get(key), str) and record[key].strip(), f'Approval requires {key}')
    require(re.fullmatch(r'/dev/dri/card[0-9]+', record.get('drm_card', '')), 'Observed DRM card required')
    require(Path(record['drm_card']).is_char_device(), 'Approved DRM device unavailable')
    require(re.fullmatch(r'[a-zA-Z0-9_,+-]+', record['keyboard_layout']), 'Invalid keyboard layout')
    sys.path.insert(0, str(APP))
    from app.config import load_device, load_script
    device = load_device(APP / 'config/device.json')
    device.validate_for_mode(mode)
    load_script(APP / 'config/script.json')
    if mode == 'live':
        require(device.sensors.hardware_verified is True, 'Live requires hardware_verified')
        require(device.sensors.pin_factory == 'lgpio', 'Live baseline requires verified lgpio')
        require(all(pin is not None for pin in device.sensors.physical_pins), 'Live requires physical pin record')
        # BCM/header correspondence, not merely five distinct numbers.
        header = {2:3, 3:5, 4:7, 14:8, 15:10, 17:11, 18:12, 27:13, 22:15,
                  23:16, 24:18, 10:19, 9:21, 25:22, 11:23, 8:24, 7:26,
                  0:27, 1:28, 5:29, 6:31, 12:32, 13:33, 19:35, 16:36,
                  26:37, 20:38, 21:40}
        require(all(header.get(bcm) == physical for bcm, physical in
                    zip(device.sensors.pins, device.sensors.physical_pins)), 'BCM/header mapping mismatch')
    if backend == 'eglfs':
        kms = json.loads(Path(display).read_text())
        require(kms.get('device') == record['drm_card'], 'KMS card differs from approval')
        require(kms.get('outputs') == [{'name': record['connector'], 'mode': '1280x720'}],
                'KMS must select exactly the approved connector at 1280x720')
    else:
        ini = configparser.ConfigParser(interpolation=None)
        ini.read(display)
        for section, key, expected in (
            ('core', 'shell', 'kiosk-shell.so'), ('core', 'idle-time', '0'),
            ('core', 'require-input', 'false'),
            ('core', 'xwayland', 'false'), ('output', 'name', record['connector']),
            ('output', 'mode', '1280x720'), ('output', 'scale', '1'),
            ('keyboard', 'keymap_layout', record['keyboard_layout'])):
            require(ini.get(section, key, fallback=None) == expected, f'Weston requires {section}.{key}={expected}')
    subprocess.run(['/usr/bin/python3', str(APP / 'deploy/preflight.py'),
                    '--display-backend', backend, '--require-pi', '--require-software',
                    '--device', str(APP / 'config/device.json')], check=True, stdout=subprocess.DEVNULL)
    return record
