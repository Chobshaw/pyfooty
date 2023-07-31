from sqlalchemy import URL

from database.engine import Database
from database.enums import Gender
from database.resource_management import SqlResourceManager
from database.schemas import (
    Team,
    TeamInstance,
    Competition,
    Season,
    Fixture,
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


resource_manager = SqlResourceManager(connection_factory=database.connection)
resource_manager.delete_all_tables()
resource_manager.create_all_tables()

with database.session() as session:
    # liverpool = TeamTable(name='liverpool', country='england', type='local', year_founded=1892)
    # man_utd = TeamTable(name='man_utd', country='england', type='local', year_founded=1893)
    # liverpool_instance = TeamInstanceTable(team=liverpool)
    # man_utd_instance = TeamInstanceTable(team=man_utd)
    prem = Competition(
        name='premier_league',
        gender='male',
        country='england',
        tier=1,
        competition_type='domestic',
        competition_format='league',
        team_type='club',
        alt_name='Premier League',
    )
    # season = SeasonTable(from_year=2022, to_year=2023)
    # anfield = VenueTable(name='anfield', country='england', city='liverpool', street='anfield_road')
    # fixture = FixtureTable(season=season, competition=prem, home_team=liverpool_instance, away_team=man_utd_instance, venue=anfield)
    # session.add_all([liverpool, man_utd, liverpool_instance, man_utd_instance, prem, season, fixture])
    session.add(prem)
    session.commit()
