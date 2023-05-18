from util import GenreUtil, DateUtil
from data.MovieEmbedData import MovieEmbedData
import interactions


def create_embed(d: MovieEmbedData):
    readable = GenreUtil.readable_genre(d.genres)
    genre_list = readable[0]
    genre_string = readable[1]
    genre_colors = {
        "Action": 0xff6961,
        "Adventure": 0xff6961,
        "Animation": 0xfdfd96,
        "Comedy": 0xA7C7E7,
        "Crime": 0x974C5E,
        "Documentary": 0x63B7B7,
        "Drama": 0xcfcfc4,
        "Foreign": 0xcfcfc4,
        "Family": 0xffb347,
        "Fantasy": 0xC3B1E1,
        "History": 0x836953,
        "Horror": 0x1D1C1A,
        "Music": 0xdaffe7,
        "Mystery": 0xD7B4F3,
        "Romance": 0xffd1dc,
        "Science Fiction": 	0xC1E1C1,
        "TV Movie": 0xcfcfc4,
        "Thriller": 0x779ecb,
        "War": 0x836953,
        "Western": 0x974C5E
    }
    embed = interactions.Embed(
        title=d.title,
        description=d.description,
        color=genre_colors[genre_list[0]],
        footer=d.tmdb_id

    )
    embed.set_thumbnail(d.thumbnail_url)
    embed.add_field(name="IMDB", value = "https://imdb.com/title/"+d.imdb_id, inline= False)
    embed.add_field(name="Release Date", value=DateUtil.readable_date(d.release_date), inline=True)
    embed.add_field(name="Listed Genre", value=genre_string, inline=True)

    return embed
