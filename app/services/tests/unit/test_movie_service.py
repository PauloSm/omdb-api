from unittest.mock import AsyncMock, call

import pytest

from app.services.movies.service import MovieService
from app.tools.base_logger import LogLevel
from app.models.movies import Movie


@pytest.mark.asyncio
async def test_get_movie_by_id_success():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    mock_movie_repository.get_movie_by_id.return_value = AsyncMock()

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie = await movie_service.get_movie_by_id("123")

    assert movie is not None, "It Should be DocumentSnapshot."
    mock_movie_repository.get_movie_by_id.assert_awaited_once_with("123"), "get_movie_by_id wasn't called correctly."
    mock_logger.log.assert_any_call(LogLevel.INFO, f"Getting movie by id: 123")

    error_call = call(LogLevel.ERROR, f"Failed to get movie by id: 123")
    assert error_call not in mock_logger.log.call_args_list, "Shouldn't log error for a successful op"


@pytest.mark.asyncio
async def test_get_movie_by_id_failure():
    mock_movie_repository = AsyncMock()
    mock_movie_repository.get_movie_by_id.side_effect = Exception("Database error")

    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie = await movie_service.get_movie_by_id("123")

    assert movie is None, "It should be None"
    mock_movie_repository.get_movie_by_id.assert_awaited_once_with("123"), "get_movie_by_id wasn't called correctly."
    mock_logger.log.assert_any_call(LogLevel.INFO, "Getting movie by id: 123")
    mock_logger.log.assert_any_call(LogLevel.ERROR, "Failed to get movie by id: 123")


@pytest.mark.asyncio
async def test_get_movie_by_title_success():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    mock_movie_repository.get_movie_by_title.return_value = AsyncMock()

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie = await movie_service.get_movie_by_title("Titanic")

    assert movie is not None, "It should DocumentSnapshot."
    mock_movie_repository.get_movie_by_title.assert_awaited_once_with("Titanic"), "get_movie_by_title wasn't called correctly."
    mock_logger.log.assert_any_call(LogLevel.INFO, f"Getting movie by title: Titanic")

    error_call = call(LogLevel.ERROR, f"Failed to get movie by title: Titanic")
    assert error_call not in mock_logger.log.call_args_list, "Shouldn't log error for a successful op"


@pytest.mark.asyncio
async def test_get_movie_by_title_failure():
    mock_movie_repository = AsyncMock()
    mock_movie_repository.get_movie_by_title.side_effect = Exception("Database error")

    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie = await movie_service.get_movie_by_title("Titanic")

    assert movie is None, "It should be None."
    mock_movie_repository.get_movie_by_title.assert_awaited_once_with("Titanic"), "get_movie_by_title wasn't called correctly."
    mock_logger.log.assert_any_call(LogLevel.INFO, "Getting movie by title: Titanic")
    mock_logger.log.assert_any_call(LogLevel.ERROR, "Failed to get movie by title: Titanic")


@pytest.mark.asyncio
async def test_create_movie_success():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    mock_movie_repository.create_movie.return_value = AsyncMock()

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie_data = {"title": "New Movie", "year": "2024"}

    result = await movie_service.create_movie(movie_data)

    assert result is not None, "It should be a DocumentSnapshot."
    mock_movie_repository.create_movie.assert_awaited_once_with(movie_data)
    mock_logger.log.assert_any_call(LogLevel.INFO, "Creating new movie entry")


@pytest.mark.asyncio
async def test_create_movie_failure():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    mock_movie_repository.create_movie.side_effect = Exception("Database error")

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie_data = {"title": "New Movie", "year": "2024"}

    result = await movie_service.create_movie(movie_data)

    assert result is None, "It should be None"
    mock_movie_repository.create_movie.assert_awaited_once_with(movie_data)
    mock_logger.log.assert_any_call(LogLevel.INFO, "Creating new movie entry")
    mock_logger.log.assert_any_call(LogLevel.ERROR, f"Failed to create movie: {movie_data}")


@pytest.mark.asyncio
async def test_delete_movie_success():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie_id = "abc123"

    await movie_service.delete_movie(movie_id)

    mock_movie_repository.delete_movie.assert_awaited_once_with(movie_id), "delete_movie wasn't called correctly."
    mock_logger.log.assert_any_call(LogLevel.INFO, f"Deleting movie: {movie_id}"), "logged i called correctly.."


@pytest.mark.asyncio
async def test_delete_movie_failure():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    mock_movie_repository.delete_movie.side_effect = Exception("Database error")

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movie_id = "abc123"

    try:
        await movie_service.delete_movie(movie_id)
        exception_raised = False
    except Exception:
        exception_raised = True

    assert not exception_raised, "It should'nt raise a exception."
    mock_movie_repository.delete_movie.assert_awaited_once_with(movie_id), "delete_movie wasn't called correctly with id."
    mock_logger.log.assert_any_call(LogLevel.INFO, f"Deleting movie: {movie_id}"), "Info Log wasn't called correctly."
    mock_logger.log.assert_any_call(LogLevel.ERROR, f"Failed to delete movie: {movie_id}"), "Error log wasn't called correctly"


@pytest.mark.asyncio
async def test_notify_empty_collection_when_empty():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    mock_movie_repository.check_empty_collection.return_value = True

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    await movie_service.notify_empty_collection()

    mock_movie_repository.check_empty_collection.assert_awaited_once(), "check_empty_collection wasn't called correctly."
    mock_pub_sub_client.publish.assert_called_once_with({"Status": "Empty"}), "publish wasn't called correctly with 'Empty' status"


@pytest.mark.asyncio
async def test_notify_empty_collection_when_not_empty():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    mock_movie_repository.check_empty_collection.return_value = False

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    await movie_service.notify_empty_collection()

    mock_movie_repository.check_empty_collection.assert_awaited_once(), "check_empty_collection wasn't called correctly."
    mock_pub_sub_client.publish.assert_not_called(), "Publish should't be called when collection is not empty"


@pytest.mark.asyncio
async def test_get_all_movies_without_start_after():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    movie_data_1 = {"Title":"Scarface","Year":"1983","Rated":"18+","Released":"09 Dec 1983","Runtime":"170 min","Genre":"Crime, Drama","Director":"Brian De Palma","Writer":"Oliver Stone, Howard Hawks, Ben Hecht","Actors":"Al Pacino, Michelle Pfeiffer, Steven Bauer","Plot":"In 1980 Miami, a determined Cuban immigrant takes over a drug cartel and succumbs to greed.","Language":"English, Spanish","Country":"United States","Awards":"8 nominations","Poster":"https://m.media-amazon.com/images/M/MV5BNjdjNGQ4NDEtNTEwYS00MTgxLTliYzQtYzE2ZDRiZjFhZmNlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"8.3/10"},{"Source":"Rotten Tomatoes","Value":"79%"},{"Source":"Metacritic","Value":"65/100"}],"Metascore":"65","imdbRating":"8.3","imdbVotes":"905,144","imdbID":"tt0086250","Type":"movie","DVD":"15 Jun 2012","BoxOffice":"$45,967,303","Production":"N/A","Website":"N/A","Response":"True"}
    expected_movies = ([Movie.from_dict(movie_data_1)], "nextToken")
    mock_movie_repository.get_all_movies.return_value = expected_movies

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movies, next_token = await movie_service.get_all_movies()

    assert movies[0].Title == movie_data_1["Title"], "The returned movie is not the asked for."
    assert next_token == "nextToken", "The returned token os not the asked for."
    mock_movie_repository.get_all_movies.assert_awaited_once_with(page_size=10, start_after=None)


@pytest.mark.asyncio
async def test_get_all_movies_with_start_after():
    mock_movie_repository = AsyncMock()
    mock_pub_sub_client = AsyncMock()
    mock_logger = AsyncMock()

    movie_data_2 = {"Title":"Yojimbo","Year":"1961","Rated":"Not Rated","Released":"13 Sep 1961","Runtime":"110 min","Genre":"Action, Drama, Thriller","Director":"Akira Kurosawa","Writer":"Akira Kurosawa, Ryûzô Kikushima","Actors":"Toshirô Mifune, Eijirô Tôno, Tatsuya Nakadai","Plot":"A crafty ronin comes to a town divided by two criminal gangs and decides to play them against each other to free the town.","Language":"Japanese","Country":"Japan","Awards":"Nominated for 1 Oscar. 4 wins & 2 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BZThiZjAzZjgtNDU3MC00YThhLThjYWUtZGRkYjc2ZWZlOTVjXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"8.2/10"},{"Source":"Rotten Tomatoes","Value":"96%"},{"Source":"Metacritic","Value":"93/100"}],"Metascore":"93","imdbRating":"8.2","imdbVotes":"130,004","imdbID":"tt0055630","Type":"movie","DVD":"23 Mar 2017","BoxOffice":"$46,808","Production":"N/A","Website":"N/A","Response":"True"}
    expected_movies = ([Movie.from_dict(movie_data_2)], "nextToken2")
    mock_movie_repository.get_all_movies.return_value = expected_movies

    movie_service = MovieService(mock_movie_repository, mock_pub_sub_client, mock_logger)

    movies, next_token = await movie_service.get_all_movies(start_after="token1")

    assert movies[0].Title == movie_data_2["Title"], "The returned movie is not the asked for."
    assert next_token == "nextToken2", "The returned token os not the asked for."
    mock_movie_repository.get_all_movies.assert_awaited_once_with(page_size=10, start_after="token1")
