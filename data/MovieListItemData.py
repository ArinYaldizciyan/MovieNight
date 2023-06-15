from dataclasses import dataclass
from typing import Optional


@dataclass
class MovieListItemData:
    tmdb_id: int
    name: Optional[str]
    guild: int
