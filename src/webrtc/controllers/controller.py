from abc import ABC, abstractmethod
from typing import List

from aiortc import RTCDataChannel

from webrtc.message import Message
from webrtc.controllers.route import Route

class Controller(ABC):
    dataChannel: RTCDataChannel
    def __init__(self, dataChannel: RTCDataChannel):
        self.dataChannel = dataChannel

    def register(self):
        self.dataChannel.on("message", self.on_message)


    def on_message(self, message: str):
        payload = Message(message)
        found = None
        for route in self.routes():
            if route.name == payload.name:
                found = route.callback
                break
        if found is not None:
            found(payload)


    @abstractmethod
    def routes(self)-> List[Route]:
        pass
