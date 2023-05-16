import requests

api_url = "https://api.themoviedb.org/3/"
image_url = "https://image.tmdb.org/t/p/"
default_image_size = "w92"


def get_image_url(movie_image_url: str, key: int):
    route_url = image_url+default_image_size+movie_image_url
    return route_url


def search(query: str, key: int):
    route_url = api_url+"/search/movie"
    params = {
        "api_key": key,
        "query": query,
        "include_adult": True
    }
    response = requests.get(route_url, params=params).json()
    print(response)
    return response


def get_info(tmdb_id: int, key: int):
    route_url = api_url+"movie/"+tmdb_id
    params = {
        "api_key": key
    }
    response = requests.get(route_url, params=params).json()
    print(response)
    return response
