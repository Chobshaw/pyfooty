from typing import Optional
from sqlalchemy import URL
from database.engine import Database
from database.repository import FootballRepository
from database.schemas import CompetitionModel
from entities.competition import Competition
from entities.season import Season, season_range
from scraping.scraper import FootballScraper
from scraping._exceptions import CompetitionNotSupportedError
from database.exceptions import CompetitionNotFoundError


class FootballDataManager:
    def __init__(
        self, scraper: FootballScraper, repository: FootballRepository
    ) -> None:
        self.scraper = scraper
        self.repository = repository

    def _get_competition(self, competition_name: str) -> Optional[Competition]:
        try:
            return self.repository.get_competition_by_name(
                name=competition_name
            )
        except CompetitionNotFoundError:
            try:
                competition = self.scraper.scrape_competition(
                    competition_name=competition_name
                )
            except CompetitionNotSupportedError:
                return
            return self.repository.add_competition(competition)

    def _process_competition_seasons(
        self,
        competition: Competition,
        from_season: Season | str | int,
        to_season: Season | str | int = Season(),
    ):
        for season in season_range(from_season, to_season):
            season = self.repository.get_or_create_season(season)
            teams = self.scraper.scrape_teams(
                competition_name=competition.name, season=season
            )
            teams = self.repository.get_or_create_teams(teams)

    def process_competitions(
        self,
        competitions: list[str],
        from_season: Season | str | int,
        to_season: Season | str | int = Season(),
    ):
        for competition_name in competitions:
            competition = self._get_competition(competition_name)
            if competition is None:
                continue
            self._process_competition_seasons(
                competition, from_season, to_season
            )


url_object = URL.create(
    drivername='mysql+mysqlconnector',
    username='footymanager',
    password='?Ch0bbyF00ty',
    host='localhost',
    port=3306,
    database='pyfooty',
)
database = Database(url_object)
data_manager = FootballDataManager(
    scraper=FootballScraper(),
    repository=FootballRepository(session_factory=database.session),
)
data_manager.process_competitions(
    ['premier_league', 'bundesliga', 'championship', 'la_liga'], 2020
)
