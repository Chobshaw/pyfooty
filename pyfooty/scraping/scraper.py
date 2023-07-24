from functools import cache, partial
import logging
import re
from typing import Iterable, Literal, Optional
import requests

import pandas as pd
from bs4 import BeautifulSoup
from entities.season import Season, season_range

from global_utils import constants
from _exceptions import SoupNotFoundError, TagNotFoundError, UrlNotFoundError

GENDER_TO_REGEX_PATTERN = {'male': r'^M$', 'female': r'^F$', 'both': r'^(M|F)$'}

logger = logging.getLogger(__name__)


@cache
def _get_soup(url: str) -> BeautifulSoup:
    data = requests.get(url)
    return BeautifulSoup(data.text, 'html.parser')


def _find_rel_url(soup: BeautifulSoup, page_string: str) -> str:
    if soup is None:
        raise SoupNotFoundError
    anchor_tag = soup.find('a', string=page_string)
    if anchor_tag is None:
        raise TagNotFoundError('a', attrs={'string': page_string})
    return anchor_tag.get('href')


@cache
def _find_url(
    parent_url: str,
    page_string: str,
    table_id: Optional[str] = None,
    *,
    base_url: Optional[str] = None,
) -> str:
    base_url = parent_url if not base_url else base_url
    soup = _get_soup(parent_url)

    try:
        if table_id is not None:
            table = soup.find('table', id=table_id)
            rel_url = _find_rel_url(table, page_string)
        else:
            rel_url = _find_rel_url(soup, page_string)
    except (SoupNotFoundError, TagNotFoundError):
        raise UrlNotFoundError(parent_url, page_string)
    return base_url + rel_url


_find_url_from_base = partial(_find_url, base_url=constants.BASE_DATA_URL)


def get_countries() -> list[str]:
    countries_url = _find_url_from_base(
        parent_url=constants.BASE_DATA_URL, page_string='Countries'
    )
    countries_df = pd.read_html(countries_url, attrs={'id': 'countries'})[0]
    return countries_df.Country.map(lambda x: x.lower()).to_list()


def get_valid_countries() -> tuple[str, ...]:
    return constants.VALID_COUNTRIES


_COMPETITIONS_URL = _find_url_from_base(
    parent_url=constants.BASE_DATA_URL, page_string='Competitions'
)


def get_competitions(
    country: Optional[str] = None,
    gender: Literal['male', 'female', 'both'] = 'male',
) -> list[str]:
    soup = _get_soup(_COMPETITIONS_URL)

    competitions = set()
    for row in soup.find_all('tr'):
        gender_data = row.find('td', attrs={'data-stat': 'gender'})
        if not gender_data or not re.match(
            GENDER_TO_REGEX_PATTERN[gender], gender_data.string
        ):
            continue

        if not country:
            competitions.add(row.th.string)
        else:
            country_data = row.find('td', attrs={'data-stat': 'country'})
            if (
                country_data
                and country_data.a
                and country in country_data.a.get('href').lower()
            ):
                competitions.add(row.th.string)

    return list(competitions)


def get_valid_competitions() -> tuple[str, ...]:
    return tuple(constants.COMPETITION_NAMES_DICT.keys())


def process_competition(
    competition: str,
    from_season: Season | str | int,
    to_season: Season | str | int = Season(),
):
    competition_url = _find_url_from_base(
        parent_url=_COMPETITIONS_URL,
        page_string=constants.COMPETITION_NAMES_DICT[competition],
    )
    soup = _get_soup(competition_url)
    for season in season_range(from_season, to_season, inclusive='both'):
        try:
            season_url = _find_url_from_base(
                parent_url=competition_url,
                page_string=str(season),
                table_id='seasons',
            )
        except UrlNotFoundError:
            logger.warning(f'No data for {season} {competition} season.')
            continue


def scrape_data(
    competitions: Iterable[str],
    from_season: Season | str | int,
    to_season: Season | str | int = Season(),
):
    for competition in competitions:
        if competition not in constants.COMPETITION_NAMES_DICT:
            logger.warning(f'Invalid competition: {competition}')
            continue
        process_competition(competition, from_season, to_season)


scrape_data(competitions=['premier_league'], from_season=2022)
