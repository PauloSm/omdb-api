from typing import Optional
from app.clients.base_db import IDocumentDB
from app.models.users import UserCreate, User, UserInDB


class UserRepository:
    def __init__(self, firestore_client: IDocumentDB):
        """
        Initializes the UserRepository with a Firestore client.

        Args:
            firestore_client (FirestoreClient): An instance of FirestoreClient.
        """
        self.firestore_client = firestore_client

    async def add_user(self, user: UserCreate) -> User:
        """
        Adds a new user to the collection.

        Args:
            user (UserCreate): The user data transfer object containing information to create a new user.

        Returns:
            User: The created user with id.
        """
        user_dict = user.dict()
        document_path = user.email
        await self.firestore_client.create_document(document_path, user_dict)
        return User(id=document_path, **user_dict)

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Get a user by email.

        Args:
            email (str): The email of the user to get.

        Returns:
            Optional[UserInDB]: The user found by the email.
        """
        document = await self.firestore_client.get_document(email)
        if document.exists:
            user_data = document.to_dict()
            user_data['hashed_password'] = user_data.pop('password')
            return UserInDB(**user_data)
        return None

    async def delete_user(self, email: str) -> None:
        """
        Deletes a user by document key (email).

        Args:
            email (str): The email of the user to delete.
        """
        await self.firestore_client.delete_document(email)
