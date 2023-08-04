from enum import Enum, StrEnum, auto


class ListedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda e: e.value, cls))


class Gender(StrEnum):
    MALE = auto()
    FEMALE = auto()


class Position(StrEnum):
    GOALKEEPER = auto()
    DEFENDER = auto()
    MIDFIELDER = auto()
    FORWARD = auto()


class CompetitionType(StrEnum):
    DOMESTIC = auto()
    INTERNATIONAL = auto()


class CompetitionFormat(StrEnum):
    FRIENDLY = auto()
    LEAGUE = auto()
    KNOCKOUT = auto()
    GROUP_KNOCKOUT = auto()


class TeamType(StrEnum):
    CLUB = auto()
    NATIONAL = auto()
