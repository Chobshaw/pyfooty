from attr import frozen

from database.enums import CompetitionFormat, CompetitionType, TeamType


@frozen
class Competition:
    name: str
    competition_type: CompetitionType
    competition_format: CompetitionFormat
    team_type: TeamType
