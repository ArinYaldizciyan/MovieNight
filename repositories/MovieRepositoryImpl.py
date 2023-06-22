from models.movieList import MovieList, MovieListItem, VoteList, VoteListItem, UserRanking
from typing import List, Optional
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData
from data.VoteListData import VoteListData
from data.VoteListItemData import VoteListItemData


class MovieRepository:
    def __init__(self):
        pass

    def create_movie_list(self, movie_list_data: MovieListData):
        MovieList.create(guild=movie_list_data.guild, library_channel_id=movie_list_data.library_channel_id)
        return True

    def add_to_list(self, movie_data: MovieListItemData):
        model = MovieListItem.get_or_create(tmdb_id=movie_data.tmdb_id, guild=movie_data.guild, name=movie_data.name)
        item = model[0]
        return MovieListItemData(id=item.id, tmdb_id=item.tmdb_id, guild=item.guild, name=item.name)

    def add_to_watched(self, movie_data: MovieListItemData):
        movie_list = MovieList.get_or_create(guild=movie_data.guild)
        MovieListItem.get_or_create(tmdb_id=movie_data.tmdb_id, movie_list=movie_data.guild, name=movie_data.name)
        return True

    def get_movie_list(self, guild: int):
        movie_list = MovieList.get_or_none(guild=guild)
        return MovieListData(guild=movie_list.guild, library_channel_id=movie_list.library_channel_id)

    def get_movie_list_items(self, guild: int, movie_id: int) -> List[MovieListItemData]:
        items = MovieListItem.select().where(MovieListItem.guild == guild and MovieListItem.id == movie_id)
        return [MovieListItemData(id=item.id, tmdb_id=item.tmdb_id, guild=item.guild, name=item.name) for item in items]

    def add_to_vote_list(self, vote_list_data: VoteListItemData):
        vote_list = VoteList.get_or_none(id=vote_list_data.vote_list_id)
        movie = MovieListItem.get_or_none(id=vote_list_data.movie_id)
        movie_title = vote_list_data.movie_title
        VoteListItem.get_or_create(vote_list=vote_list, movie=movie, movie_title=movie_title)
        return True

    def get_vote_list(self, vote_list_data: VoteListData):
        vote_list = VoteList.get_or_create(guild=vote_list_data.guild, created_by_user=vote_list_data.created_by_user)
        item = vote_list[0]
        return VoteListData(id=item.id, guild=item.guild, created_by_user=item.created_by_user)

    def get_vote_list_items(self, vote_list_id: int) -> List[VoteListItemData]:
        items = VoteListItem.select().where(VoteListItem.vote_list == vote_list_id)
        return [VoteListItemData(
            vote_list_item_id=item.id,
            vote_list_id=item.vote_list,
            movie_id=item.movie,
            movie_title=item.movie_title) for item in items]

    def add_to_ranking(self, vote_list_item_id: int, user: int, ranking: int):
        user_ranking = UserRanking.get_or_none(vote_movie=vote_list_item_id, user=user)
        if user_ranking:
            user_ranking.ranking = ranking
            user_ranking.save()
        else:
            UserRanking.create(vote_movie=vote_list_item_id, user=user, ranking=ranking)
        return True
