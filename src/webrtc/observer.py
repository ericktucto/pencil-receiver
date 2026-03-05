import json
from typing import Dict, List
from aiortc import RTCDataChannel, RTCPeerConnection

from webrtc.controllers import controllers
from webrtc.controllers.controller import CallableRoute, Controller
from webrtc.messages.message import Message


class Observer():

    peer = None
    controllers: List[Controller] = []
    routes: Dict[str, CallableRoute] = {}

    def __init__(self, peer: RTCPeerConnection):
        self.peer = peer
        self.peer.on("datachannel", self.on_datachannel)
        self.peer.on("connectionstatechange", self.on_connectionstatechange)

    def on_datachannel(self, channel: RTCDataChannel):
        try:
            print("Data Channel opened", channel.label)

            self.controllers = [c(channel) for c in controllers]
            self.routes = {}

            for controller in self.controllers:
                self.routes.update(controller.routes())

            @channel.on("message")
            def on_message(message: str):
                self.on_message(channel, message)

            @channel.on("close")
            def on_close():
                print("DataChannel closed")

        except Exception as e:
            channel.send(json.dumps({
                'name': 'error',
                'except': 'error en el servidor'
            }))
            print("DEBUG: Exception", e)

    def on_message(self, channel: RTCDataChannel, message: str):
        payload = Message(message)

        handler = self.routes.get(payload.name)

        if handler:
            try:
                handler(payload, channel)
            except Exception as e:
                print("handler error:", e)

    async def on_connectionstatechange(self):
        if self.peer:
            print("Connection state is %s" % self.peer.connectionState)
        if self.peer and self.peer.connectionState == 'closed':
            await self.peer.close()
            self.peer = None

