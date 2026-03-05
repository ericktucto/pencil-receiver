import inspect
import json
from typing import Callable, Dict
from aiortc import RTCDataChannel

from webrtc.messages.message import Message

CallableRoute = Callable[[Message, RTCDataChannel], None]

class Controller:
    dataChannel: RTCDataChannel

    def __init__(self, channel: RTCDataChannel):
        self.dataChannel = channel

    def routes(self) -> Dict[str, Callable]:

        routes = {}

        for _, method in inspect.getmembers(self, inspect.ismethod):

            route_name = getattr(method, "_route_name", None)
            message_type = getattr(method, "_message_type", None)

            if route_name:
                if message_type:
                    def _method(msg: Message, dataChannel: RTCDataChannel):
                        data = json.dumps(msg._payload)
                        if message_type:
                            method(message_type(data), dataChannel)

                    routes[route_name] = _method
                    continue
                routes[route_name] = method

        return routes
