from datetime import date
from typing import Optional, Self

from sqlalchemy import (
    LargeBinary,
    String,
    Date,
    ForeignKey,
    Integer,
    Enum,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    composite,
)

from database.enums import (
    Gender,
    Position,
    TeamType,
    CompetitionType,
    CompetitionFormat,
)
from database.sqlalchemy_dict_mixin import SqlAlchemyDictMixin
from entities.competition import (
    Competition,
    CompetitionUrlInfo,
    get_competition_dict,
)
from entities.entity import Entity
from entities.season import Season


class BaseModel(DeclarativeBase, SqlAlchemyDictMixin):
    @property
    def entity_type(self) -> type[Entity]:
        raise NotImplementedError(
            'Corresponding entity type has not been set for '
            f'model: {self.__class__}.'
        )

    @classmethod
    def from_entity(cls, entity: Entity) -> Self:
        return cls.from_dict(entity.to_dict(deep=False))

    def to_entity(self) -> Entity:
        return self.entity_type.from_dict(self.to_dict())


class PlayerModel(BaseModel):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date_of_birth: Mapped[date] = mapped_column(Date())
    country: Mapped[str] = mapped_column(String(30))


class PlayerInstanceModel(BaseModel):
    __tablename__ = 'player_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('player.id'))
    team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))
    position: Mapped[Position] = mapped_column(Enum(Position))

    player: Mapped['PlayerModel'] = relationship()
    team: Mapped['TeamInstanceModel'] = relationship(back_populates='players')


class TeamModel(BaseModel):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    country: Mapped[str] = mapped_column(String(30))
    type: Mapped[TeamType] = mapped_column(Enum(TeamType))
    year_founded: Mapped[int] = mapped_column(Integer())
    logo: Mapped[Optional[LargeBinary]] = mapped_column(LargeBinary())


class TeamInstanceModel(BaseModel):
    __tablename__ = 'team_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))

    team: Mapped['TeamModel'] = relationship()
    players: Mapped[list['PlayerInstanceModel']] = relationship(
        back_populates='team'
    )


class CompetitionModel(BaseModel):
    __tablename__ = 'competition'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), index=True)
    alt_name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    country: Mapped[Optional[str]] = mapped_column(String(30))
    tier: Mapped[Optional[int]] = mapped_column(Integer)
    competition_type: Mapped[CompetitionType] = mapped_column(
        Enum(CompetitionType)
    )
    competition_format: Mapped[CompetitionFormat] = mapped_column(
        Enum(CompetitionFormat)
    )
    team_type: Mapped[TeamType] = mapped_column(Enum(TeamType))
    url_number: Mapped[int] = mapped_column(Integer)
    url_name: Mapped[str] = mapped_column(String(30))

    url_info: Mapped[CompetitionUrlInfo] = composite('url_number', 'url_name')

    @property
    def entity_type(self) -> type[Entity]:
        return Competition


class SeasonModel(BaseModel):
    __tablename__ = 'season'

    id: Mapped[int] = mapped_column(primary_key=True)
    from_year: Mapped[int] = mapped_column(Integer())
    to_year: Mapped[int] = mapped_column(Integer())

    @property
    def entity_type(self) -> type[Entity]:
        return Season


class FixtureModel(BaseModel):
    __tablename__ = 'fixture'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date())
    season_id: Mapped[int] = mapped_column(ForeignKey('season.id'))
    competition_id: Mapped[int] = mapped_column(ForeignKey('competition.id'))
    home_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    away_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    game_week: Mapped[int] = mapped_column(Integer())
    venue: Mapped[str] = mapped_column(String(30))

    season: Mapped['SeasonModel'] = relationship(foreign_keys=season_id)
    competition: Mapped['CompetitionModel'] = relationship(
        foreign_keys=competition_id
    )
    home_team: Mapped['TeamInstanceModel'] = relationship(
        foreign_keys=home_team_id
    )
    away_team: Mapped['TeamInstanceModel'] = relationship(
        foreign_keys=away_team_id
    )


if __name__ == '__main__':
    competition_dict = get_competition_dict()
    competition = competition_dict['premier_league']
    model = CompetitionModel.from_entity(competition)
    pass
