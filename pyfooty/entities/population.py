from typing import Optional
from attrs import define, field
from database.schemas import Competition, Season, Team


@define
class Population:
    competition: Optional[Competition] = None
    season: Optional[Season] = None
    teams: Optional[dict[str, Team]] = field(default={})
