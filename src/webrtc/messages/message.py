from abc import ABC
import json


class Message(ABC):
    def __init__(self, payload: str):
        self._payload = json.loads(payload)
        self._data = self._payload['data']


    @property
    def name(self) -> str:
        return self._payload['name']

    @property
    def data(self):
        return self._payload['data']

