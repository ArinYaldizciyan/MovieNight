from dataclasses import dataclass
from typing import Optional


@dataclass
class VoteListData:
    id: Optional[int]
    guild: int
    created_by_user: int
