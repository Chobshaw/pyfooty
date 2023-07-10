from enum import Enum


class ListedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda e: e.value, cls))


class Position(ListedEnum):
    GOALKEEPER = 'goalkeeper'
    DEFENDER = 'defender'
    MIDFIELDER = 'midfielder'
    FORWARD = 'forward'


class CompetitionType(ListedEnum):
    DOMESTIC = 'domestic'
    INTERNATIONAL = 'international'


class CompetitionFormat(ListedEnum):
    FRIENDLY = 'friendly'
    LEAGUE = 'league'
    KNOCKOUT = 'knockout'
    GROUP_KNOCKOUT = 'group_knockout'


class TeamType(ListedEnum):
    LOCAL = 'local'
    NATIONAL = 'national'
