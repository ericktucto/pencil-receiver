import asyncio
from collections import namedtuple
from typing import Set
from aiortc import RTCPeerConnection
from webrtc.mouse import VirtualMouse
from webrtc.observer import Observer

Listen = namedtuple("Listen", ["peer"])
MOUSE_PATH = '/dev/input/event9'

class App:
    observer: Observer | None = None
    mouse: VirtualMouse
    listeners: Set[Listen] = set()
    task = None

    def __init__(self):
        self.mouse = VirtualMouse(MOUSE_PATH)

    async def start(self):
        await self.mouse.start()


    async def add_peer(self, peer: RTCPeerConnection):
        if self.observer:
            await self.observer.destroy()
        self.observer = Observer(peer, self.mouse)

    def add_listener(self, pc: RTCPeerConnection):
        self.listeners.add(Listen(pc))

    async def destroy(self):
        if self.observer:
            await self.observer.destroy()
            self.observer = None
        coros = [l.peer.close() for l in self.listeners]
        await asyncio.gather(*coros)
        self.listeners.clear()
        if self.task is not None:
            self.task.cancel('Terminate')
