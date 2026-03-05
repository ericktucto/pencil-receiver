import asyncio
from collections import namedtuple
from typing import Callable
from evdev import UInput, ecodes as e, InputDevice

from mouse import Coords

Listen = namedtuple("Listen", ["peer"])

CallableObserver = Callable[[Listen|None, Coords], None]

class VirtualMouse:
    currentCoords = Coords(0, 0)

    def __init__(self, input: str):

        capabilities = {
            e.EV_REL: (e.REL_X, e.REL_Y),
            e.EV_KEY: (e.BTN_LEFT,)
        }

        self.ui = UInput(capabilities, name="virtual-drag-mouse")

        self._last_x: float | None = None
        self._last_y: float | None = None

        self._moved = False
        self._pressed = False

        # evita jitter del dedo
        self._threshold = 1

        self.device = InputDevice(input)
        self.task = None

    async def start(self):
        self.task = asyncio.create_task(
            self.observer_mouse(self.device, self.handle_mouse)
        )


    async def observer_mouse(self, device: InputDevice, callback: CallableObserver):
        try:
            async for event in device.async_read_loop():
                if event.type == e.EV_REL:
                    if event.code == e.REL_X:
                        self.__setX(1 if event.value > 0 else -1)

                    elif event.code == e.REL_Y:
                        self.__setY(1 if event.value > 0 else -1)
                callback(None, self.currentCoords)
        finally:
            device.close()


    def __setX(self, add: int):
        self.currentCoords = Coords(
            self.currentCoords.x + add,
            self.currentCoords.y
        )

    def __setY(self, add: int):
        self.currentCoords = Coords(
            self.currentCoords.x,
            self.currentCoords.y + add
        )

    def handle_mouse(self, listen, coords: Coords):
        print("COORDS", coords)

    # -------------------------
    # DOWN
    # -------------------------

    def down(self, x: float, y: float):

        self._last_x = x
        self._last_y = y

        self._moved = False
        self._pressed = True

        # presionar botón
        self.ui.write(e.EV_KEY, e.BTN_LEFT, 1)
        self.ui.syn()

    # -------------------------
    # MOVE
    # -------------------------

    def move(self, x: float, y: float):

        if self._last_x is None or self._last_y is None:
            self._last_x = x
            self._last_y = y
            return

        dx = x - self._last_x
        dy = y - self._last_y

        self._last_x = x
        self._last_y = y

        # aplicar threshold
        if abs(dx) < self._threshold and abs(dy) < self._threshold:
            return

        self._moved = True

        dx = int(dx)
        dy = int(dy)

        if dx != 0:
            self.ui.write(e.EV_REL, e.REL_X, dx)

        if dy != 0:
            self.ui.write(e.EV_REL, e.REL_Y, dy)

        self.ui.syn()

    # -------------------------
    # UP
    # -------------------------

    def up(self):

        if not self._pressed:
            return

        # si hubo drag → soltar
        if self._moved:
            self.ui.write(e.EV_KEY, e.BTN_LEFT, 0)

        # si fue tap → click
        else:
            self.ui.write(e.EV_KEY, e.BTN_LEFT, 1)
            self.ui.write(e.EV_KEY, e.BTN_LEFT, 0)

        self.ui.syn()

        self._pressed = False
        self._last_x = None
        self._last_y = None
        self._moved = False

    # -------------------------
    # CLOSE
    # -------------------------

    def close(self):
        self.ui.close()
