from enum import Enum


class ListedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda e: e.value, cls))


class Position(Enum):
    GOALKEEPER = 'goalkeeper'
    DEFENDER = 'defender'
    MIDFIELDER = 'midfielder'
    FORWARD = 'forward'


class CompetitionType(Enum):
    DOMESTIC = 'domestic'
    INTERNATIONAL = 'international'


class CompetitionFormat(Enum):
    FRIENDLY = 'friendly'
    LEAGUE = 'league'
    KNOCKOUT = 'knockout'
    GROUP_KNOCKOUT = 'group_knockout'


class TeamType(Enum):
    LOCAL = 'local'
    NATIONAL = 'national'
