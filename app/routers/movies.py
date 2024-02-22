from fastapi import HTTPException, Query, Path, APIRouter, BackgroundTasks, Security

from app.services.movies.service import MovieService
from app.repositories.movies.repository import MovieRepository
from app.clients.firestore.firestore import get_firestore_client
from app.clients.pub_sub.pub_sub import get_pub_sub_client
from app.models.movies import Movie
from app.models.pagination import Page
from app.tools.logger import APPLogger
from app.routers.dependencies import get_current_user

router = APIRouter()

logger = APPLogger()
firestore_client = get_firestore_client(logger=logger)
pub_sub_client = get_pub_sub_client(logger)
movie_repository = MovieRepository(firestore_client)
movie_service = MovieService(movie_repository, pub_sub_client, logger)


@router.get("/get-all-movies", response_model=Page[Movie])
async def list_movies_paginated(page_size: int = Query(10, ge=1), start_after: str = Query(None)):
    try:
        movies, next_page_token = await movie_service.get_all_movies(page_size=page_size, start_after=start_after)
        return Page(items=movies, next_page_token=next_page_token, page_size=len(movies))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/by-id/{movie_id}/", response_model=Movie)
async def get_movie_by_id(movie_id: str = Path(...)):
    movie = await movie_service.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie id not found")
    return movie.to_dict()


@router.get("/title/", response_model=Movie)
async def get_movie_by_title(title: str = Query(...)):
    movie = await movie_service.get_movie_by_title(title)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie.to_dict()


@router.post("/", response_model=Movie)
async def create_movie(movie_data: Movie):
    created_movie = await movie_service.create_movie(movie_data.dict())
    return created_movie.to_dict()


@router.delete("/{movie_id}/", status_code=204)
async def delete_movie(movie_id: str, current_user: str = Security(get_current_user)):
    await movie_service.delete_movie(movie_id)
    return {"detail": "Movie deleted successfully"}


@router.post("/notify-if-empty/")
async def notify_empty_collection(background_tasks: BackgroundTasks):
    """
    Checks if the movie collection is empty and notifies via Pub/Sub if it is.
    """
    background_tasks.add_task(movie_service.notify_empty_collection)
    return {"message": "Database check in progress"}
