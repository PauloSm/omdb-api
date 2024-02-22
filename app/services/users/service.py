from datetime import timedelta
from app.models.users import UserCreate
from app.auth.utils import get_password_hash, verify_password, create_access_token
from app.repositories.users.repository import UserRepository
from app.tools.base_logger import ILogger, LogLevel

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserService:
    def __init__(self, user_repository: UserRepository, logger: ILogger):
        self.user_repository = user_repository
        self.logger = logger

    async def create_user(self, user_in: UserCreate):
        hashed_password = get_password_hash(user_in.password)
        user_in.password = hashed_password
        try:
            return await self.user_repository.add_user(user_in)
        except Exception:
            self.logger.log(LogLevel.ERROR, f"Failed to create user: {user_in.email}")

    async def authenticate_user(self, email: str, password: str):
        user_in_db = await self.user_repository.get_user_by_email(email)
        if user_in_db and verify_password(password, user_in_db.hashed_password):
            return user_in_db
        return None

    def create_token_for_user(self, user_email: str):
        try:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_email}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        except Exception:
            self.logger.log(LogLevel.ERROR, f"Failed to create access token for user: {user_email}")
