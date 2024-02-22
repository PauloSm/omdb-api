from typing import Optional, Tuple, List

from app.repositories.movies.repository import IMovieRepository, DocumentSnapshot
from app.clients.base_message_service import IMessageService
from app.tools.base_logger import ILogger, LogLevel
from app.models.movies import Movie


class MovieService:
    def __init__(self, movie_repository: IMovieRepository, pub_sub_client: IMessageService, logger: ILogger):
        """
        Initializes the MovieService with a movie repository and a pub/sub client.

        Args:
            movie_repository (IMovieRepository): An instance of a class that implements the IMovieRepository interface.
            pub_sub_client (IMessageService): An instance of a class that implements the IMessageService interface.
        """
        self.movie_repository = movie_repository
        self.pub_sub_client = pub_sub_client
        self.logger = logger

    async def get_all_movies(self, page_size: int = 10, start_after: str = None) -> Tuple[List[Movie], Optional[str]]:
        return await self.movie_repository.get_all_movies(page_size=page_size, start_after=start_after)

    async def get_movie_by_id(self, movie_id: str) -> Optional[DocumentSnapshot]:
        self.logger.log(LogLevel.INFO, f"Getting movie by id: {movie_id}")
        try:
            return await self.movie_repository.get_movie_by_id(movie_id)
        except Exception:
            self.logger.log(LogLevel.ERROR, f"Failed to get movie by id: {movie_id}")

    async def get_movie_by_title(self, title: str) -> Optional[DocumentSnapshot]:
        self.logger.log(LogLevel.INFO, f"Getting movie by title: {title}")
        try:
            return await self.movie_repository.get_movie_by_title(title)
        except Exception:
            self.logger.log(LogLevel.ERROR, f"Failed to get movie by title: {title}")

    async def create_movie(self, movie_data: dict) -> DocumentSnapshot:
        self.logger.log(LogLevel.INFO, f"Creating new movie entry")
        try:
            return await self.movie_repository.create_movie(movie_data)
        except Exception:
            self.logger.log(LogLevel.ERROR, f"Failed to create movie: {movie_data}")

    async def delete_movie(self, movie_id: str) -> None:
        self.logger.log(LogLevel.INFO, f"Deleting movie: {movie_id}")
        try:
            await self.movie_repository.delete_movie(movie_id)
        except Exception as e:
            self.logger.log(LogLevel.ERROR, f"Failed to delete movie: {movie_id}")

    async def notify_empty_collection(self):
        """
        Check if the movie collection is empty and notify via the publish-subscribe client if it is.
        """
        is_empty = await self.movie_repository.check_empty_collection()
        if is_empty:
            self.pub_sub_client.publish({"Status": "Empty"})
