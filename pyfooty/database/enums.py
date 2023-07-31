from enum import Enum
from typing import Self


class ListedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda e: e.value, cls))


class ExtendedEnum(Enum):
    @classmethod
    def from_value(cls, value: str) -> Self:
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f'Value not found in enum: {cls.__name__}')


class Gender(ExtendedEnum):
    MALE = 'male'
    FEMALE = 'female'


class Position(Enum):
    GOALKEEPER = 'goalkeeper'
    DEFENDER = 'defender'
    MIDFIELDER = 'midfielder'
    FORWARD = 'forward'


class CompetitionType(ExtendedEnum):
    DOMESTIC = 'domestic'
    INTERNATIONAL = 'international'


class CompetitionFormat(ExtendedEnum):
    FRIENDLY = 'friendly'
    LEAGUE = 'league'
    KNOCKOUT = 'knockout'
    GROUP_KNOCKOUT = 'group_knockout'


class TeamType(ExtendedEnum):
    CLUB = 'club'
    NATIONAL = 'national'
