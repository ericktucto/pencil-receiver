import json
from typing import Dict


class Message():
    def __init__(self, payload: str):
        self._payload = json.loads(payload)


    @property
    def name(self) -> str:
        return self._payload['name']

    @property
    def data(self) -> Dict:
        return self._payload['data']
