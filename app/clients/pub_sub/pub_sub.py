import json
from typing import Any, Dict
from functools import lru_cache

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError

from app.tools.tools import get_project_id
from app.tools.base_logger import ILogger, LogLevel
from app.tools.config import Config
from app.clients.base_message_service import IMessageService


class PubSubClient(IMessageService):
    def __init__(self, logger: ILogger):
        self.project_id = get_project_id()
        self.topic_name = Config.PUB_SUB_TOPIC_NAME()
        self.publisher = pubsub_v1.PublisherClient()
        self.logger = logger

    def get_topic_path(self) -> str:
        """Generate the full topic path."""
        return self.publisher.topic_path(self.project_id, self.topic_name)

    def publish(self, message: Dict[str, Any]) -> None:
        """Publish a message to a Pub/Sub topic."""
        topic_path = self.get_topic_path()
        message_bytes = json.dumps(message).encode("utf-8")
        try:
            future = self.publisher.publish(topic_path, message_bytes)
            future.result()
        except GoogleAPICallError as e:
            self.logger.log(LogLevel.ERROR, f"Failed to publish message to topic {self.topic_name}")


@lru_cache
def get_pub_sub_client(logger: ILogger) -> PubSubClient:
    return PubSubClient(logger)
