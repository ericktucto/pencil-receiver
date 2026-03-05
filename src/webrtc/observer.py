from aiortc import RTCPeerConnection

from webrtc.controllers import controllers


class Observer():

    peer = None

    def __init__(self, peer: RTCPeerConnection):
        self.peer = peer
        self.peer.on("datachannel", self.on_datachannel)
        self.peer.on("connectionstatechange", self.on_connectionstatechange)


    def on_datachannel(self, channel):
        print("Data Channel opened", channel.label)
        for c in controllers:
            print("DEBUG: ", c)
            controller = c(channel)
            controller.register()


    async def on_connectionstatechange(self):
        if self.peer:
            print("Connection state is %s" % self.peer.connectionState)
        if self.peer and self.peer.connectionState == 'closed':
            await self.peer.close()
            self.peer = None

