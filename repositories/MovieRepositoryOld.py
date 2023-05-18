import abc
from models import movieList
from data import MovieListItemData


class MovieRepository(abc.ABC):
    @abc.abstractmethod
    def add_to_list(self, guild: MovieListItemData) -> bool:
        raise NotImplementedError
