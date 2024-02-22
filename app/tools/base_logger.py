from abc import ABC, abstractmethod
from enum import Enum, auto


class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class ILogger(ABC):
    @abstractmethod
    def log(self, level: LogLevel, message: str):
        pass
