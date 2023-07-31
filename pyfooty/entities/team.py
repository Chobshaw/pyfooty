from attr import frozen

from database.enums import TeamType


@frozen
class Team:
    name: str
    country: str
    type: TeamType
    year_founded: int
