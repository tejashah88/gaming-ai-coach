from abc import ABC, abstractmethod


class BaseTTS(ABC):
    @abstractmethod
    def speak(self, text: str):
        pass

    @abstractmethod
    def cleanup(self):
        pass
