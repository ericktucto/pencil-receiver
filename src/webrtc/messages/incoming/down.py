from webrtc.messages.message import Message

class DownMessage(Message):
    @property
    def x(self) -> int:
        return int(self._payload['data']['x'])

    @property
    def y(self) -> int:
        return int(self._payload['data']['y'])
