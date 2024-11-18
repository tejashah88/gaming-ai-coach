from abc import ABC, abstractmethod


class BaseTTS(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass
