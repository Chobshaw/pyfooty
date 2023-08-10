import json
from pathlib import Path
from typing import Optional

from attrs import field, frozen, validators

from database.enums import (
    CompetitionFormat,
    CompetitionType,
    Gender,
    TeamType,
)
from entities.entity import Entity


@frozen
class CompetitionUrlInfo(Entity):
    number: int
    name: str

    def __composite_values__(self) -> tuple[int, str]:
        return self.number, self.name


@frozen(kw_only=True)
class Competition(Entity):
    id: Optional[int] = field(default=None)
    name: str
    alt_name: str
    gender: Gender
    team_type: TeamType
    competition_type: CompetitionType = field()
    competition_format: CompetitionFormat = field()
    country: Optional[str] = field(
        default=None, validator=validators.optional(validators.instance_of(str))
    )
    tier: Optional[int] = field(
        default=None,
        validator=validators.optional(
            [validators.instance_of(int), validators.ge(1)]
        ),
    )
    url_info: CompetitionUrlInfo

    def __str__(self) -> str:
        return (
            f'Competition with name: {self.name}, and country: {self.country}'
        )

    @country.validator
    def _check_country(self, attribute, value) -> None:
        if self.team_type == TeamType.NATIONAL and value is not None:
            raise ValueError(
                'Country attribute must be None if team_type is national'
            )

    @competition_type.validator
    def _check_competition_type(self, attribute, value) -> None:
        if (
            self.team_type == TeamType.NATIONAL
            and value is not CompetitionType.INTERNATIONAL
        ):
            raise ValueError(
                'competition_type must be international '
                'if team_type is national'
            )

    @tier.validator
    def _check_tier(self, attribute, value) -> None:
        if (
            self.competition_format == CompetitionFormat.FRIENDLY
            and value is not None
        ):
            raise ValueError(
                'Tier attribute must be None if competition_format is friendly'
            )


def get_competition_dict() -> dict[str, Competition]:
    pyfooty_path = Path(__file__).parent.parent
    competitions_file_path = pyfooty_path / 'global_utils/competitions.json'
    with open(competitions_file_path, 'r') as file:
        competitions_dict = json.load(file)
    for competition_name, data in competitions_dict.items():
        competitions_dict[competition_name] = Competition.from_dict(data)
    return competitions_dict


if __name__ == '__main__':
    competition_dict = get_competition_dict()
    for name, competition in competition_dict.items():
        print(name, repr(competition))
        print(competition.to_dict(deep=False))
