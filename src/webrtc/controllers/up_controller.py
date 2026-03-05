from webrtc.controllers.controller import Controller

class UpController(Controller):
    def up(self, message):
        print("Message from server: " + message)

    def register(self):
        print("registrando")
        self.dataChannel.on("up", self.up)

