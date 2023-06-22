from dataclasses import dataclass
from typing import Optional

@dataclass
class WatchSourceData:
    torrents: Optional[list[dict]]
    providers: Optional[list[dict]]
