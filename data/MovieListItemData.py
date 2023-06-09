from dataclasses import dataclass
from typing import Optional


@dataclass
class MovieListItemData:
    id: Optional[int]
    tmdb_id: int
    name: Optional[str]
    guild: int
