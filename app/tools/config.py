import os


class Config:
    @staticmethod
    def LOG_NAME():
        return os.getenv('LOG_NAME', 'default')

    @staticmethod
    def ACCESS_TOKEN_TTL_MINUTES():
        return os.getenv('ACCESS_TOKEN_TTL_MINUTES', "30")

    @staticmethod
    def TOKEN_SECRET_KEY():
        return os.getenv('TOKEN_SECRET_KEY')

    @staticmethod
    def TOKEN_ALGORITHM():
        return os.getenv('TOKEN_ALGORITHM')

    @staticmethod
    def MOVIES_COLLECTION_NAME():
        # Firestore Movies collection name
        return os.getenv('MOVIES_COLLECTION_NAME', 'movies')

    @staticmethod
    def USERS_COLLECTION_NAME():
        # Firestore Users collection name
        return os.getenv('USERS_COLLECTION_NAME', 'users')

    @staticmethod
    def PUB_SUB_TOPIC_NAME():
        return os.getenv('PUB_SUB_TOPIC_NAME', 'database-check-topic')
