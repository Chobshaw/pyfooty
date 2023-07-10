from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session

from mysql_database.database import Database
from mysql_database.resource_management import SqlResourceManager
from mysql_database.schemas import Team, TeamInstance, Competition, Season, Venue, Fixture, Base

engine = create_engine('mysql+mysqlconnector://fpl_manager:?Ch0b!F4nt4sy@localhost:3306/fpl_database')

url_object = URL.create(
    drivername='mysql+mysqlconnector',
    username='fpl_manager',
    password='?Ch0b!F4nt4sy',
    host='localhost',
    port=3306,
    database='fpl_database',
)
database = Database(url_object)


resource_manager = SqlResourceManager(connection_factory=database.connection)
resource_manager.create_all_tables()

with Session(engine) as session:
    liverpool = Team(name='liverpool', country='england', type='local', year_founded=1892)
    man_utd = Team(name='man_utd', country='england', type='local', year_founded=1893)
    liverpool_instance = TeamInstance(team=liverpool)
    man_utd_instance = TeamInstance(team=man_utd)
    prem = Competition(name='premier_league', competition_type='domestic', competition_format='league', team_type='local')
    season = Season(from_year=2022, to_year=2023)
    anfield = Venue(name='anfield', country='england', city='liverpool', street='anfield_road')
    fixture = Fixture(season=season, competition=prem, home_team=liverpool_instance, away_team=man_utd_instance, venue=anfield)
    session.add_all([liverpool, man_utd, liverpool_instance, man_utd_instance, prem, season, fixture])
    session.commit()
