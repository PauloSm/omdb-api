from typing import List, Optional
from pydantic import BaseModel


class Rating(BaseModel):
    Source: str
    Value: str


class Movie(BaseModel):
    Title: str
    Year: str
    Rated: Optional[str]
    Released: Optional[str]
    Runtime: Optional[str]
    Genre: Optional[str]
    Director: Optional[str]
    Writer: Optional[str]
    Actors: Optional[str]
    Plot: Optional[str]
    Language: Optional[str]
    Country: Optional[str]
    Awards: Optional[str]
    Poster: Optional[str]
    Ratings: Optional[List[Rating]]
    Metascore: Optional[str]
    imdbRating: Optional[str]
    imdbVotes: Optional[str]
    imdbID: str
    Type: Optional[str]
    DVD: Optional[str]
    BoxOffice: Optional[str]
    Production: Optional[str]
    Website: Optional[str]
    Response: Optional[bool]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
