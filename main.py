import uvicorn
from fastapi import FastAPI

from app.routers.movies import router as movies_router
from app.routers.auth import router as auth_router

app = FastAPI(title="Movies API")

app.include_router(movies_router, prefix="/v1/movies", tags=["movies"])
app.include_router(auth_router, prefix="/v1/movies", tags=["auths"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
