from typing import List
from interactions import Modal, ShortText


def create_ranking_modal(movies: List) -> Modal:
    modal = Modal(title="Movie Ranking")
    components = [ShortText(label=movie[0], custom_id=movie[1]) for movie in movies]
    modal.add_components(*components)
    return modal
