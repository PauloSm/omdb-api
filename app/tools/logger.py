import logging

from google.cloud import logging as cloud_logging

from app.tools.base_logger import ILogger, LogLevel
from app.tools.config import Config


class APPLogger(ILogger):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(APPLogger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.client = cloud_logging.Client()
        self.client.setup_logging()
        self.logger = logging.getLogger(Config.LOG_NAME())
        self.logger.setLevel(logging.INFO)

    def log(self, level: LogLevel, message: str, **kwargs):
        log_method = {
            LogLevel.DEBUG: self.logger.debug,
            LogLevel.INFO: self.logger.info,
            LogLevel.WARNING: self.logger.warning,
            LogLevel.ERROR: self.logger.error,
            LogLevel.CRITICAL: self.logger.critical,
        }.get(level, self.logger.info)

        log_method(message)
