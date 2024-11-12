from abc import ABC, abstractmethod


class BaseTTS(ABC):
    @abstractmethod
    def speak(self, text):
        pass

    @abstractmethod
    def cleanup(self):
        pass
