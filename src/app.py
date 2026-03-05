import asyncio
from collections import namedtuple
import json
from typing import Callable, Set
from aiortc import RTCDataChannel, RTCPeerConnection
from evdev import InputDevice, ecodes
from mouse import Coords
from webrtc.observer import Observer

Listen = namedtuple("Listen", ["peer"])

class App:
    observer: Observer
    listeners: Set[Listen] = set()
    task = None
    currentCoords = Coords(0, 0)

    def add_peer(self, peer: RTCPeerConnection):
        self.observer = Observer(peer)

    def add_listener(self, pc: RTCPeerConnection):
        self.listeners.add(Listen(pc))

    async def destroy(self):
        coros = [l.peer.close() for l in self.listeners]
        await asyncio.gather(*coros)
        self.listeners.clear()
        if self.task is not None:
            self.task.cancel('Terminate')

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


    async def __observer_mouse(self, device: InputDevice, callback: Callable[[Listen, Coords], None]):
        try:
            async for event in device.async_read_loop():
                print("event: ", event.type)
                if event.type == ecodes.EV_REL:
                    if event.code == ecodes.REL_X:
                        self.__setX(event.value)
                    elif event.code == ecodes.REL_Y:
                        self.__setY(event.value)

                    for l in self.listeners:
                        callback(l, self.currentCoords)
        finally:
            device.close()


    def observer_mouse(self, device: InputDevice, callback: Callable[[Listen, Coords], None]):
        self.task = asyncio.create_task(self.__observer_mouse(device, callback))
