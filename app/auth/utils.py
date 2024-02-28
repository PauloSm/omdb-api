from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from app.tools.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(Config.ACCESS_TOKEN_TTL_MINUTES()))
    to_encode.update({"exp": expire})
    # TODO google create secret manager client and add secret key there
    encoded_jwt = jwt.encode(to_encode, Config.TOKEN_SECRET_KEY(), algorithm=Config.TOKEN_ALGORITHM())
    return encoded_jwt
