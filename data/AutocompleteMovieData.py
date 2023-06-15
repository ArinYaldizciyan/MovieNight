from dataclasses import dataclass
from typing import Iterable


@dataclass
class AutocompleteMovieData:
    movies: Iterable[str | int | float | dict[str, int | float | str]]
