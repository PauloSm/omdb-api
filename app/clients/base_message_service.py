from abc import ABC, abstractmethod
from typing import Any, Dict


class IMessageService(ABC):
    @abstractmethod
    def get_topic_path(self) -> str:
        pass

    @abstractmethod
    def publish(self, message: Dict[str, Any]) -> None:
        pass
