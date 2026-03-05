from webrtc.controllers.controller import Controller

class DownController(Controller):
    def down(self, message):
        print("Message from server: " + message)

    def register(self):
        self.dataChannel.on("down", self.down)
