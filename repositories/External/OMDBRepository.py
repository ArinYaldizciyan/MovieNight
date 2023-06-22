import requests
from appCore.ParamManager import ParamManager
from models.movieList import MovieList, MovieListItem


class OMDBRepository():
    # Todo: Add all dependencies into constructor
    def __init__(self):
        self.p = ParamManager()
        self.api_url: str = self.p.get_parameter(name='OMDB_API_URL', from_environment=True)
        self.api_key: str = self.p.get_parameter(name='OMDB_API_KEY', from_environment=True)

    def search(self, imdb_id: str):
        route_url = self.api_url
        params = {
            "api_key": self.api_key,
            "i": imdb_id,
        }
        response = requests.get(route_url, params=params).json()
        return response

    def get_oscar_info(self, imdb_id: str):
        response = self.search(imdb_id)
        return response

    def get_imdb_rating(self, imdb_id: str):
        response = self.search(imdb_id)
        return response


