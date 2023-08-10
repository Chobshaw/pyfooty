from __future__ import annotations

from typing import Iterator, Literal, Optional, Self
from attrs import frozen, field, validators
from entities.utils import get_current_year

from scraping._local_utils import _split_on_dash_or_endash

MINIMUM_VALID_YEAR = 2_000
ENDASH = chr(8211)


@frozen(order=True)
class Season:
    id: Optional[int] = field(default=None, kw_only=True, order=False)
    from_year: int = field(
        converter=int,
        validator=[
            validators.instance_of(int),
            validators.ge(MINIMUM_VALID_YEAR),
        ],
    )
    to_year: int = field(converter=int, validator=validators.instance_of(int))

    def __str__(self) -> str:
        return f'{self.from_year}-{self.to_year}'

    @from_year.default
    def _from_year_factory(self) -> int:
        return get_current_year()

    @to_year.default
    def _to_year_factory(self) -> int:
        return self.from_year + 1

    @to_year.validator
    def _check_to_year(self, attribute, value) -> None:
        if value != self.from_year + 1:
            raise ValueError(
                'to_year must be exactly 1 year greater than from_year'
            )

    @classmethod
    def from_string(cls, season: str) -> Self:
        split_season = [int(year) for year in _split_on_dash_or_endash(season)]
        if len(split_season) == 1:
            return cls(split_season[0])
        return cls(split_season[0], split_season[1])

    def to_string(self, dash_type: Literal['dash', 'endash'] = 'dash') -> str:
        if dash_type not in ('dash', 'endash'):
            raise ValueError(
                'Argument, dash_type, should be one of: dash, endash'
            )
        if dash_type == 'dash':
            return self.__str__()
        return f'{self.from_year}{ENDASH}{self.to_year}'

    def increment(self, years: int) -> Season:
        return Season(self.from_year + years)

    def next(self) -> Season:
        return self.increment(years=1)

    def previous(self) -> Season:
        return self.increment(years=-1)


def convert_to_season(
    season_repr: Optional[Season | str | int] = None,
) -> Season:
    if isinstance(season_repr, Season):
        return season_repr
    if isinstance(season_repr, int):
        return Season(season_repr)
    if isinstance(season_repr, str):
        return Season.from_string(season_repr)
    raise TypeError(f'Cannot convert type: {type(season_repr)} to Season')


def season_range(
    start: Season | int | str,
    end: Optional[Season | int | str] = Season(),
    inclusive: Literal['left', 'right', 'both', 'neither'] = 'both',
) -> Iterator[Season]:
    start = convert_to_season(start)
    end = convert_to_season(end)

    # Make sure from_season is not greater than to_season
    if start > end:
        raise ValueError('from_season cannot be greater than to_season.')

    include_start = inclusive in ('both', 'left')
    include_end = inclusive in ('both', 'right')

    # Generate all seasons from from_season to to_season (inclusive)
    current_season = start if include_start else start.next()
    end = end if include_end else end.previous()
    while current_season <= end:
        yield current_season

        # Increment to the next season
        current_season = current_season.next()
