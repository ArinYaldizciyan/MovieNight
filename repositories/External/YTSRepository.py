import requests


class YTSRepository:
    #Todo: Add all dependencies into constructor
    def __init__(self):
        self.api_url = "https://yts.mx/api/v2/list_movies.json"

    def search(self, imdb_id: str):
        route_url = self.api_url
        params = {
            "query": imdb_id
        }
        response = requests.get(route_url, params=params).json()
        return response

    def get_torrents(self, imdb_id: str):
        trackers = [
            "udp://open.demonii.com:1337/announce",
            "udp://tracker.openbittorrent.com:80",
            "udp://tracker.coppersurfer.tk:6969",
            "udp://glotorrents.pw:6969/announce",
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://torrent.gresille.org:80/announce",
            "udp://tracker.leechers-paradise.org:6969",

        ]
        response = self.search(imdb_id)

        torrent_list = response["data"]["movies"][0]["torrents"]
        torrent_urls = []
        for torrent in torrent_list:
            torrent_urls.append(torrent["url"])

        return torrent_list

    def get_magnet_links(self, imdb_id: str):

        # magnet:?xt=urn:btih:578261664906C00F43603D9BFBED8B84207B410B&dn=Batman+Begins&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80
        torrent_list = self.get_torrents(imdb_id)
        magnet_list = []
        # for torrent in torrent_list:

