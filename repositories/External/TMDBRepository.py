import requests
from appCore.ParamManager import ParamManager
from models.movieList import MovieList, MovieListItem


class TMDBRepository():
    # Todo: Add all dependencies into constructor
    def __init__(self):
        self.p = ParamManager()
        self.api_url: str = self.p.get_parameter(name='TMDB_API_URL', from_environment=True)
        self.api_key: str = self.p.get_parameter(name='TMDB_API_KEY', from_environment=True)
        self.image_url: str = self.p.get_parameter(name='TMDB_IMAGE_URL', from_environment=True)
        self.default_image_size: str = self.p.get_parameter(name='TMDB_DEFAULT_IMAGE_SIZE', from_environment=True)

    def get_image_url(self, movie_image_url: str):
        route_url = self.image_url + self.default_image_size + movie_image_url
        return route_url

    def search(self, query: str):
        route_url = self.api_url + "/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
            "include_adult": True
        }
        response = requests.get(route_url, params=params).json()
        print(response)
        return response

    def get_info(self, tmdb_id: int):
        # Todo: Certain movies cause errors. Assuming it has to do with the format of the response,
        #  or maybe the type of movie
        route_url = self.api_url + "movie/" + str(tmdb_id)
        params = {
            "api_key": self.api_key
        }
        response = requests.get(route_url, params=params).json()
        print(response)
        return response

