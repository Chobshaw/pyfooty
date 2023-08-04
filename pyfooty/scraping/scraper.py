import logging
import re
from typing import Iterable, Literal
import requests
from entities.competition import Competition, get_competition_dict

from entities.season import Season, season_range

from global_utils import constants
from scraping._local_utils import _get_soup, _find_url_from_base
from scraping._exceptions import UrlNotFoundError, CompetitionNotSupportedError

logger = logging.getLogger(__name__)

ScrapingLocation = Literal[
    'england', 'france', 'germany', 'italy', 'portugal', 'spain'
]


def _has_team_name(tag):
    return tag.name == 'p' and tag.strong and 'Team Name' in tag.get_text()


class FootballScraper:
    LOCATION_URL_EXTENSION_DICT = {
        'england': 'en',
        'france': 'fr',
        'germany': 'de',
        'italy': 'it',
        'portugal': 'pt',
        'spain': 'es',
    }
    COMPETITION_DICT = get_competition_dict()
    _COMPETITIONS_URL = _find_url_from_base(
        parent_url=constants.BASE_DATA_URL, page_string='Competitions'
    )

    def __init__(self, *, location: ScrapingLocation = 'england') -> None:
        self.location_url = self.LOCATION_URL_EXTENSION_DICT.get(location)
        if self.location_url is None:
            raise ValueError(f'Invalid location: {location}.')

    def process_team(self, team_url: str):
        team_data_url = _find_url_from_base(
            parent_url=team_url,
            page_string=re.compile(r'Stats & History$'),
        )
        team_data_soup = _get_soup(team_data_url)
        logo_image = team_data_soup.find('img', class_='teamlogo')
        logo_data = requests.get(logo_image.get('src')).content
        data_div = logo_image.parent.next_sibling
        p_tag = data_div.find(_has_team_name)

    def process_teams(self, season_url: str):
        soup = _get_soup(season_url)
        team_table = soup.find('table', id=re.compile(r'^results'))
        for team in team_table.find_all('td', attrs={'data-stat': 'team'})[:1]:
            team_url = constants.BASE_DATA_URL + team.a.get('href')
            self.process_team(team_url)

    def process_season(self, season: Season, competition_url: str):
        self.population.season = season
        try:
            season_url = _find_url_from_base(
                parent_url=competition_url,
                page_string=str(season),
                table_id='seasons',
            )
        except UrlNotFoundError:
            logger.warning(
                f'No data available for '
                f'{season} {self.population.competition.name} season.'
            )
            return
        self.process_teams(season_url)

    def process_competition(
        self,
        competition: Competition,
        from_season: Season | str | int,
        to_season: Season | str | int = Season(),
    ):
        self.population.competition = competition
        competition_url = _find_url_from_base(
            parent_url=self._COMPETITIONS_URL,
            page_string=competition.alt_name,
        )
        for season in season_range(from_season, to_season, inclusive='both'):
            self.process_season(season, competition_url)

    def scrape_data(
        self,
        competition_names: Iterable[str],
        from_season: Season | str | int,
        to_season: Season | str | int = Season(),
    ):
        competition_dict = get_competition_dict()
        for competition_name in competition_names:
            competition = competition_dict.get(competition_name)
            if competition is None:
                logger.warning(f'Invalid competition: {competition_name}')
                continue
            self.process_competition(competition, from_season, to_season)

    def scrape_competition(self, competition_name: str) -> Competition:
        competition = self.COMPETITION_DICT.get(competition_name)
        if competition is None:
            raise CompetitionNotSupportedError(competition_name)
        return competition
