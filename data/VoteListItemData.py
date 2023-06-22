from dataclasses import dataclass
from typing import Optional

@dataclass
class VoteListItemData:
    vote_list_item_id: Optional[int]
    vote_list_id: int
    movie_id: int
    movie_title: str
