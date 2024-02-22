from typing import Optional, Tuple, List
from abc import ABC, abstractmethod

from google.cloud.firestore_v1 import DocumentSnapshot

from app.clients.base_db import IDocumentDB
from app.models.movies import Movie


class IMovieRepository(ABC):
    @abstractmethod
    async def get_all_movies(self, page_size: int):
        pass

    @abstractmethod
    async def get_movie_by_id(self, movie_id: str):
        pass

    @abstractmethod
    async def get_movie_by_title(self, title):
        pass

    @abstractmethod
    async def create_movie(self, document: dict):
        pass

    @abstractmethod
    async def delete_movie(self, movie_id: str):
        pass

    @abstractmethod
    async def check_empty_collection(self):
        pass


class MovieRepository(IMovieRepository):
    def __init__(self, firestore_client: IDocumentDB):
        """
        Initializes the MovieRepository with a Firestore client.

        Args:
            firestore_client (IDocumentDB): An instance of a class that implements the IDocumentDB interface.
        """
        self.firestore_client = firestore_client

    async def get_all_movies(self, page_size: int = 10, start_after: str = None) -> Tuple[List[Movie], Optional[str]]:
        docs, next_page_token = await self.firestore_client.get_paginated_documents(page_size=page_size,
                                                                                    start_after=start_after)
        movies = [Movie.from_dict(doc.to_dict()) for doc in docs]
        return movies, next_page_token

    async def get_movie_by_id(self, movie_id: str) -> Optional[DocumentSnapshot]:
        """
        Get a movie by ID.

        Args:
            movie_id (str): The ID of the movie to get.

        Returns:
            Optional[DocumentSnapshot]: The DocumentSnapshot of the requested movie.
        """
        return await self.firestore_client.get_document(movie_id)

    async def get_movie_by_title(self, title) -> Optional[DocumentSnapshot]:
        """
        Get a single movie by title.

        Args:
            title (str): The title of the movie.

        Returns:
            Optional[DocumentSnapshot]: The DocumentSnapshot of the movie.
        """
        return await self.firestore_client.get_document_by_title(title)

    async def create_movie(self, document: dict) -> DocumentSnapshot:
        """
        Create a new movie document.

        Args:
            document (dict): A dictionary containing the movie data.

        Returns:
            DocumentSnapshot: A DocumentSnapshot of the created movie document.
        """
        imdb_id = document.get("imdbID")
        return await self.firestore_client.create_document(imdb_id, document)

    async def delete_movie(self, movie_id: str) -> None:
        """
        Delete a movie by ID.

        Args:
            movie_id (str): The ID of the movie to delete.
        """
        await self.firestore_client.delete_document(movie_id)

    async def check_empty_collection(self) -> bool:
        """
        Check if the movie collection is empty.

        Returns:
            bool: True if the collection is empty, False otherwise.
        """
        return await self.firestore_client.is_collection_empty()
