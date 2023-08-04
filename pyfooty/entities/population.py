from typing import Optional
from attrs import define, field
from database.schemas import CompetitionModel, SeasonModel


@define
class Population:
    competition: Optional[CompetitionModel] = None
    season: Optional[SeasonModel] = None
