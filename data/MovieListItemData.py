from dataclasses import dataclass


@dataclass
class MovieListItemData:
    tmdb_id: int
    name: str
    guild: int
