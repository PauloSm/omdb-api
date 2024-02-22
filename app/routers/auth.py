from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.services.users.service import UserService
from app.models.users import UserCreate
from app.repositories.users.repository import UserRepository
from app.clients.firestore.firestore import get_firestore_client
from app.tools.logger import APPLogger
from app.tools.config import Config


router = APIRouter()

logger = APPLogger()
firestore_client = get_firestore_client(logger, Config.USERS_COLLECTION_NAME())
user_repository = UserRepository(firestore_client)
user_service = UserService(user_repository, logger)


@router.post("/signup")
async def signup(user_in: UserCreate):
    user = await user_service.create_user(user_in)
    if not user:
        raise HTTPException(status_code=400, detail="Error when creating the user")
    return {"email": user.email}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Wrong email or password.")
    return user_service.create_token_for_user(user.email)
