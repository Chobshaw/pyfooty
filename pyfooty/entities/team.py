from typing import Optional
from attrs import frozen, field, validators

from database.enums import Gender, TeamType
from entities.entity import Entity
from entities.utils import get_current_year


@frozen(kw_only=True)
class Team(Entity):
    id: Optional[int] = field(default=None)
    name: str
    gender: Gender
    country: str
    type: TeamType
    year_founded: int = field(
        default=None,
        validator=validators.optional(
            [validators.instance_of(int), validators.le(get_current_year())]
        ),
    )
