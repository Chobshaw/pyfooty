from sqlalchemy import URL

from database.engine import Database
from database.enums import Gender, TeamType
from database.schemas import (
    CompetitionModel,
    SeasonModel,
    TeamInstanceModel,
    TeamModel,
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

with database.session() as session:
    liverpool = TeamModel(
        id=1,
        name='liverpool',
        gender=Gender.MALE,
        country='england',
        type=TeamType.CLUB,
        year_founded=1892,
    )
    # man_utd = TeamTable(name='man_utd', country='england', type='local', year_founded=1893)
    liverpool_instance = TeamInstanceModel(id=2, team=liverpool)
    # man_utd_instance = TeamInstanceTable(team=man_utd)
    prem = CompetitionModel(
        name='premier_league',
        gender='male',
        country='england',
        tier=1,
        competition_type='domestic',
        competition_format='league',
        team_type='club',
    )
    # season = SeasonTable(from_year=2022, to_year=2023)
    # fixture = FixtureTable(season=season, competition=prem, home_team=liverpool_instance, away_team=man_utd_instance, venue=anfield)
    # session.add_all([liverpool, man_utd, liverpool_instance, man_utd_instance, prem, season, fixture])
    session.add(liverpool_instance)
    session.commit()
