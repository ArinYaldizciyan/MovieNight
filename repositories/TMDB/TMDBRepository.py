import abc, requests
from models.movieList import MovieList, MovieListItem


class TMDBRepository:
    #Todo: Add all dependencies into constructor
    def __init__(self):
        self.api_url = "https://api.themoviedb.org/3/"
        self.image_url = "https://image.tmdb.org/t/p/"
        self.default_image_size = "w92"

    def get_image_url(self, movie_image_url: str, key: int):
        route_url = self.image_url + self.default_image_size + movie_image_url
        return route_url

    def search(self, query: str, key: int):
        route_url = self.api_url + "/search/movie"
        params = {
            "api_key": key,
            "query": query,
            "include_adult": True
        }
        response = requests.get(route_url, params=params).json()
        print(response)
        return response

    def get_info(self, tmdb_id: int, key: int):
        # Todo: Certain movies cause errors. Assuming it has to do with the format of the response,
        #  or maybe the type of movie
        route_url = self.api_url + "movie/" + str(tmdb_id)
        params = {
            "api_key": key
        }
        response = requests.get(route_url, params=params).json()
        print(response)
        return response

