from collections.abc import Iterable

from sqlalchemy import and_, select

from database.engine import SessionFactory
from database.exceptions import CompetitionNotFoundError
from database.schemas import BaseModel, CompetitionModel, SeasonModel
from entities.competition import Competition
from entities.entity import Entity
from entities.season import Season


class FootballRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self.session_factory = session_factory

    def _add_entity(
        self, entity: Entity, model_type: type[BaseModel]
    ) -> Entity:
        model = model_type.from_entity(entity)
        with self.session_factory() as session:
            session.add(model)
            session.commit()
            # session.refresh(entity_model)
            return model.to_entity()

    def add_competition(self, competition: Competition) -> Competition:
        return self._add_entity(entity=competition, model_type=CompetitionModel)

    def get_competition_by_name(self, name: str) -> Competition:
        with self.session_factory() as session:
            competition_model = session.scalars(
                select(CompetitionModel).where(CompetitionModel.name == name)
            ).first()
            if not competition_model:
                raise CompetitionNotFoundError(name)
            return competition_model.to_entity()

    def add_season(self, season: Season) -> Season:
        return self._add_entity(entity=season, model_type=SeasonModel)

    def _get_or_create_entity(
        self, entity: Entity, model: BaseModel, fields: Iterable[str]
    ) -> Entity:
        with self.session_factory() as session:
            entity_model = session.scalars(
                select(model).where(
                    and_(
                        getattr(model, field) == getattr(entity, field)
                        for field in fields
                    )
                )
            ).one_or_none()
        if entity_model:
            return entity_model.to_entity()
        return self._add_entity(entity=entity, model_type=model)

    def get_or_create_season(self, season: Season) -> Season:
        return self._get_or_create_entity(
            entity=season, model=SeasonModel, fields=['from_year']
        )
