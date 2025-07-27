from abc import ABC, abstractmethod

class LoggingInterface(ABC):
    @abstractmethod
    def log(self, level: str, message: str):
        pass

