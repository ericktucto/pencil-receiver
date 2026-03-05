from abc import ABC, abstractmethod

class Controller(ABC):
    dataChannel = None
    def __init__(self, dataChannel):
        dataChannel = dataChannel

    @abstractmethod
    def register(self):
        pass
