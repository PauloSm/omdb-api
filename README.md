# OMDB API

## Application Structure

The application is organized into three main directories that separate the application's responsibilities, improving maintenance and scalability.

- **routers**: Contains the API endpoints. Each route is defined in a separate file (`movies.py` for movies and `auth.py` for authentication), facilitating the organization of related functionalities.
- **services**: Service layer containing the business logic. The functions here call the corresponding methods in the repository layer to access and manipulate data.
- **repositories**: Repository layer that abstracts data access. This layer interacts directly with the database clients or any other data source.

## Using the API

### Authentication

- **Signup**: `POST /v1/auth/signup` - Create a new user account.
- **Login**: `POST /v1/auth/login` - Authenticate in the application to obtain an access token.

### Movies Management

- **List all movies**: `GET /v1/movies/get-all-movies` - Receive a paginated list of all movies.
- **Search movie by ID**: `GET /v1/movies/by-id/{movie_id}/` - Get details of a specific movie by its ID.
- **Search movie by title**: `GET /v1/movies/title/` - Get details of a movie by title.
- **Create new movie**: `POST /v1/movies/` - Add a new movie to the collection.
- **Delete movie**: `DELETE /v1/movies/{movie_id}/` - Remove a movie from the collection.

### Notifications and Background Tasks

- **Notify if the collection is empty**: `POST /v1/movies/notify-if-empty/` - Checks in the background if the movie collection is empty and notifies via Pub/Sub if it is.
