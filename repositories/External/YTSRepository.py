import requests
from typing import Optional, List

class YTSRepository:
    #Todo: Add all dependencies into constructor
    def __init__(self):
        self.api_url = "https://yts.mx/api/v2/list_movies.json"
        self.detail_api_url = "https://yts.mx/api/v2/movie_details.json"

    def search(self, imdb_id: str):
        route_url = self.api_url
        params = {
            "query_term": imdb_id,
            "limit": 10
        }
        response = requests.get(route_url, params=params).json()
        return response

    def get(self, imdb_id: str) -> Optional[List]:
        route_url = self.detail_api_url
        params = {
            "imdb_id": imdb_id,
            "with_images": False,
            "with_cast": False
        }
        response = requests.get(route_url, params=params).json()
        trackers = [
            "udp://open.demonii.com:1337/announce",
            "udp://tracker.openbittorrent.com:80",
            "udp://tracker.coppersurfer.tk:6969",
            "udp://glotorrents.pw:6969/announce",
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://torrent.gresille.org:80/announce",
            "udp://tracker.leechers-paradise.org:6969",

        ]

        torrent_list = response["data"]["movie"]["torrents"]
        torrent_urls = []
        for torrent in torrent_list:
            torrent_urls.append(torrent["url"])

        return torrent_list

    def get_magnet_links(self, imdb_id: str):

        # magnet:?xt=urn:btih:578261664906C00F43603D9BFBED8B84207B410B&dn=Batman+Begins&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80
        torrent_list = self.get_torrents(imdb_id)
        magnet_list = []
        # for torrent in torrent_list:

