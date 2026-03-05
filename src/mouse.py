import time
from collections import namedtuple
from typing import List
from evdev import UInput, ecodes as e, InputDevice, list_devices

Coords = namedtuple("Coords", ["x", "y"])

def move_mouse(x: int, y: int):
    capabilities = {
        e.EV_REL: (e.REL_X, e.REL_Y),
        e.EV_KEY: (e.BTN_LEFT, ),
    }

    ui = UInput(capabilities, name="virtual-drag-mouse")

    # 🔒 Presionar botón izquierdo (mantener presionado)
    ui.write(e.EV_KEY, e.BTN_LEFT, 1)
    ui.syn()

    time.sleep(0.2)

    print("moviendo mouse")
    ui.write(e.EV_REL, e.REL_X, x)
    ui.write(e.EV_REL, e.REL_Y, y)
    ui.syn()

    time.sleep(0.2)

    # 🔓 Soltar botón
    ui.write(e.EV_KEY, e.BTN_LEFT, 0)
    ui.syn()

    ui.close()


def devices()-> List[InputDevice]:
    return [InputDevice(path) for path in list_devices()]


def devices_to_dict(devices: List[InputDevice]):
    d = []
    for device in devices:
        d.append({
            'name': device.name,
            'path': device.path
        })
    return d

