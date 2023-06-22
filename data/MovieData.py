from dataclasses import dataclass


@dataclass
class MovieData:
    title: str
    description: str
    release_date: str
    genres: list[object]
    poster_path: str
    imdb_id: str
    tmdb_id: int
    thumbnail_url: str
    director: str