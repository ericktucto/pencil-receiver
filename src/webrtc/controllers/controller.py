import inspect
import json
from typing import Callable, Dict
from aiortc import RTCDataChannel

from webrtc.messages.message import Message
from webrtc.mouse import VirtualMouse

CallableRoute = Callable[[Message, RTCDataChannel], None]

class Controller:
    dataChannel: RTCDataChannel
    mouse: VirtualMouse

    def __init__(self, channel: RTCDataChannel, mouse: VirtualMouse):
        self.dataChannel = channel
        self.mouse = mouse

    def routes(self) -> Dict[str, Callable]:

        routes = {}

        for _, method in inspect.getmembers(self, inspect.ismethod):

            route_name = getattr(method, "_route_name", None)
            message_type = getattr(method, "_message_type", None)

            if route_name:

                if message_type:

                    def make_handler(method, message_type):

                        def _method(msg: Message, dataChannel: RTCDataChannel):
                            data = json.dumps(msg._payload)
                            method(message_type(data), dataChannel)

                        return _method

                    routes[route_name] = make_handler(method, message_type)
                else:
                    routes[route_name] = method
        return routes
