from typing import Callable

from webrtc.messages.message import Message


class Route():
    def __init__(self, name: str, callback: Callable[[Message], None]):
        self.name = name
        self.callback = callback

