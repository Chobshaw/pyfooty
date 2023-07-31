from sqlalchemy import URL
from database.engine import Database
from database.repository import FootballRepository
from entities.season import Season
from scraping.scraper import FootballScraper
from database.exceptions import CompetitionNotFoundError


class FootballDataManager:
    def __init__(
        self, scraper: FootballScraper, repository: FootballRepository
    ) -> None:
        self.scraper = scraper
        self.repository = repository

    def process_competitions(
        self,
        competitions: list[str],
        from_season: Season | str | int,
        to_season: Season | str | int = Season(),
    ):
        for competition_name in competitions:
            try:
                competition = self.repository.get_competition_by_name(
                    name=competition_name
                )
            except CompetitionNotFoundError:
                competition_data = self.scraper.scrape_competition(
                    competition_name=competition_name
                )
                competition = self.repository.add_competition(competition_data)
            pass


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
data_manager.process_competitions(['premier_league'], 2020)
