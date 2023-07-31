from sqlalchemy import select
from database.engine import SessionFactory
from database.exceptions import CompetitionNotFoundError
from database.schemas import Competition
from entities.competition import CompetitionData


class FootballRepository:
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory

    def add_competition(self, data: CompetitionData) -> Competition:
        competition = Competition.from_data(data)
        with self.session_factory() as session:
            session.add(competition)
            session.commit()
            session.refresh(competition)
            return competition

    def get_competition_by_name(self, name: str) -> Competition:
        with self.session_factory() as session:
            competition = session.scalars(
                select(Competition).where(Competition.name == name)
            ).first()
            if not competition:
                raise CompetitionNotFoundError(name)
            return competition
