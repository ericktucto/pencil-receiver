from webrtc.messages.message import Message

class CoordsMessage(Message):
    @property
    def x(self) -> float:
        return self._payload['data']['x']

    @property
    def y(self) -> float:
        return self._payload['data']['y']
