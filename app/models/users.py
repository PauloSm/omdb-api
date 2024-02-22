from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(BaseModel):
    email: str
    password: str


class User(UserBase):
    # pensar melhor sobre essa definição
    pass


class UserInDB(BaseModel):
    email: str
    hashed_password: str
