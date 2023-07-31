import json
from pathlib import Path
from typing import Optional
from attrs import field, frozen, validators

from database.enums import (
    CompetitionFormat,
    CompetitionType,
    Gender,
    TeamType,
    ExtendedEnum,
)


def str_to_enum(string: str, enum: ExtendedEnum) -> ExtendedEnum:
    return enum.from_value(string)


@frozen
class CompetitionData:
    name: str
    alt_name: str
    gender: Gender = field(converter=lambda x: str_to_enum(x, Gender))
    team_type: TeamType = field(converter=lambda x: str_to_enum(x, TeamType))
    competition_type: CompetitionType = field(
        converter=lambda x: str_to_enum(x, CompetitionType)
    )
    competition_format: CompetitionFormat = field(
        converter=lambda x: str_to_enum(x, CompetitionFormat)
    )
    country: Optional[str] = field(
        default=None, validator=validators.optional(validators.instance_of(str))
    )
    tier: Optional[int] = field(
        default=None,
        validator=validators.optional(
            [validators.instance_of(int), validators.ge(1)]
        ),
    )

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


def get_competition_dict() -> dict[str, CompetitionData]:
    pyfooty_path = Path(__file__).parent.parent
    competitions_file_path = pyfooty_path / 'global_utils/competitions.json'
    with open(competitions_file_path, 'r') as file:
        competitions_dict = json.load(file)
    for competition_name, data in competitions_dict.items():
        competitions_dict[competition_name] = CompetitionData(**data)
    return competitions_dict


for key, val in get_competition_dict().items():
    print(key, str(val), repr(val))
