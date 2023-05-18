import interactions
from interactions import AutocompleteContext, Button, ButtonStyle, PartialEmoji
from repositories.TMDB.TMDBRepository import TMDBRepository
from util import EmbedUtil
from data.MovieEmbedData import MovieEmbedData


class SearchMovieUsecase:

    # Todo: Dependency injection
    def __init__(self):
        self.tmdb_repository = TMDBRepository()

    # Todo: Abstract the embed creation into a view. I.E return an embed view,
    #  this should be based on some embed dataclass
    async def execute(self, movie_id: int, tmdb_key: int) -> list:
        info = self.tmdb_repository.get_info(movie_id, tmdb_key)
        thumbnail_url = self.tmdb_repository.get_image_url(info["poster_path"], tmdb_key)
        embed_data = MovieEmbedData(title=info["original_title"], description=info["overview"],
                                    release_date=info["release_date"], genres=info["genres"],
                                    poster_path=info["poster_path"], imdb_id=info["imdb_id"],
                                    thumbnail_url=thumbnail_url, tmdb_id=movie_id)
        embed = EmbedUtil.create_embed(embed_data)

        add_emoji = PartialEmoji(name="➕")
        add = interactions.Button(style=interactions.ButtonStyle.GREEN, custom_id='add_to_list', emoji=add_emoji)
        eye_emoji = PartialEmoji(name="👁️")
        watched = interactions.Button(style=interactions.ButtonStyle.BLUE, custom_id='add_to_watched', emoji=eye_emoji)
        action_row = interactions.ActionRow(add, watched)

        return [embed, action_row]
