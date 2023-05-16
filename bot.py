import interactions
from interactions import Client, Intents, listen, slash_command, slash_option, \
    OptionType, SlashContext, Modal, ShortText, ParagraphText, ModalContext, AutocompleteContext, InteractionContext
import parameters, tmdb
from datetime import datetime
import requests
from models.movieList import *

bot = Client(intents=Intents.ALL, debug_scope=833127429853806592)


@listen()
async def on_ready():
    print("Ready!")

@slash_command(
    name="about",
    description="Get Information about a Movie!"
)
@slash_option(
    name="movie",
    description="Movie to lookup",
    required=True,
    opt_type=OptionType.STRING,
    autocomplete=True
)
async def search(ctx: InteractionContext, movie: int):
    await ctx.defer(ephemeral=False)
    info = tmdb.get_info(movie, tmdb_key)
    embed = _create_embed(info["original_title"], info["overview"],
                          info["release_date"], info["genres"], info["poster_path"], info["imdb_id"])
    await ctx.send(embeds=[embed])


@search.autocomplete("movie")
async def autocomplete(ctx: AutocompleteContext):
    await default_movie_autocomplete(ctx)


async def default_movie_autocomplete(ctx: AutocompleteContext, arg_index: int = 0):
    typed = ctx.args[arg_index]
    movies = []
    if typed:
        raw_movies = tmdb.search(typed, tmdb_key)["results"]
        for movie in raw_movies:
            movies.append({
                "name": movie["original_title"],
                "value": movie["id"]}
            )
    await ctx.send(
        choices=movies
    )


def _add_movie(movie_name):
    char = Movie.get_or_create(name=movie_name)
    char.save()


def _create_embed(title: str, description: str, release_date: str, genres: list[object], poster_path: str, imdb_id: str):
    embed = interactions.Embed(
        title=title,
        description=description,
    )
    embed.set_thumbnail(tmdb.get_image_url(poster_path, tmdb_key))
    embed.add_field(name="IMDB", value = "https://imdb.com/title/"+imdb_id, inline= False)
    embed.add_field(name="Release Date", value=_readable_date(release_date), inline=True)
    embed.add_field(name="Listed Genre", value=_readable_genre(genres), inline=True)

    return embed


def _readable_date(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%B %dth, %Y")
    return formatted_date


def _readable_genre(genre_ids):
    genres = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        10770: "TV Movie",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }

    genre_list = []
    for genre in genre_ids:
        genre_list.append(genre["name"])
    genre_string = ', '.join(genre_list)
    return genre_string


def initialize_db():
    with db:
        db.create_tables([MovieList, Tag], safe=True)


initialize_db()
db = SqliteDatabase('movienight.db')
p = parameters.Parameter()
key = p.get_parameter(name='DISCORD_BOT_KEY', from_environment=True)
tmdb_key = p.get_parameter(name='TMDB_API_KEY', from_environment=True)
bot.start(key)
