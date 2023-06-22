from util import GenreUtil, DateUtil
from data.MovieData import MovieData
from typing import Union, Dict
from typing import List
from interactions import PartialEmoji, EmbedFooter, ActionRow, Button, ButtonStyle, BaseContext
import interactions


def create_about_movie_embed(d: MovieData) -> interactions.Embed:
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
        "Science Fiction": 0xC1E1C1,
        "TV Movie": 0xcfcfc4,
        "Thriller": 0x779ecb,
        "War": 0x836953,
        "Western": 0x974C5E
    }
    embed = interactions.Embed(
        title=d.title,
        description=d.description,
        color=genre_colors[genre_list[0]]
    )
    embed.set_footer(text=str(d.tmdb_id) + "|" + str(d.imdb_id), icon_url=None)
    embed.set_thumbnail(d.thumbnail_url)
    embed.add_field(name="Director", value=d.director, inline=True)
    embed.add_field(name="IMDB", value="https://imdb.com/title/" + d.imdb_id, inline=False)
    embed.add_field(name="Release Date", value=DateUtil.readable_date(d.release_date), inline=True)
    embed.add_field(name="Listed Genre", value=genre_string, inline=True)

    return embed


def create_vote_starter_embed(vote_list_id: Union[str, int]) -> Dict:
    embed = interactions.Embed(
        title="Rank Movies",
        description="Click the button below to start ranking the movies!"
    )
    # embed.set_footer(text=str(vote_list_id), icon_url=None)
    vote_emoji = PartialEmoji.from_str("📨")
    vote_button = interactions.Button(
        label="Rank Movies",
        style=interactions.ButtonStyle.BLURPLE,
        custom_id='start_ranking|' + str(vote_list_id),
        emoji=vote_emoji)

    finish_vote_emoji = PartialEmoji.from_str("☑️")
    finish_vote_button = interactions.Button(
        label="Finish Ranking",
        style=interactions.ButtonStyle.GREEN,
        custom_id='finish_ranking|' + str(vote_list_id),
        emoji=finish_vote_emoji)

    return {"embed": embed, "components": ActionRow(vote_button, finish_vote_button)}
