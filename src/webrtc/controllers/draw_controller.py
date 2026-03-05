from aiortc import RTCDataChannel
from webrtc.controllers.controller import Controller
from webrtc.messages.message import Message
from webrtc.messages.incoming.coords import CoordsMessage
from webrtc.messages.incoming.down import DownMessage
from webrtc.router import route

class DrawController(Controller):

    @route("down")
    def down(self, message: DownMessage, _: RTCDataChannel):
        print("Message from server: ", message)

    @route("coords")
    def coords(self, message: CoordsMessage, _: RTCDataChannel):
        print("Message from server: ", message)

    @route("up")
    def up(self, message: Message, _: RTCDataChannel):
        print("Message from server: ", message)

