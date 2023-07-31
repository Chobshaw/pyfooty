from datetime import date
from typing import ClassVar, Optional, Self

from sqlalchemy import LargeBinary, String, Date, ForeignKey, Integer, Enum
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    mapped_column,
    relationship,
)

from database.enums import (
    Gender,
    Position,
    TeamType,
    CompetitionType,
    CompetitionFormat,
)
from entities.competition import CompetitionData
from entities.entity import Entity


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date_of_birth: Mapped[date] = mapped_column(Date())
    country: Mapped[str] = mapped_column(String(30))


class PlayerInstance(Base):
    __tablename__ = 'player_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('player.id'))
    team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))
    position: Mapped[Position] = mapped_column(Enum(Position))

    player: Mapped['Player'] = relationship()
    team: Mapped['TeamInstance'] = relationship(back_populates='players')


class Team(Base):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    country: Mapped[str] = mapped_column(String(30))
    type: Mapped[TeamType] = mapped_column(Enum(TeamType))
    year_founded: Mapped[int] = mapped_column(Integer())
    logo: Mapped[LargeBinary] = mapped_column(LargeBinary())


class TeamInstance(Base):
    __tablename__ = 'team_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))

    team: Mapped['Team'] = relationship()
    players: Mapped[list['PlayerInstance']] = relationship(
        back_populates='team'
    )


class Competition(Base):
    __tablename__ = 'competition'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    country: Mapped[Optional[str]] = mapped_column(String(30))
    tier: Mapped[Optional[int]] = mapped_column(Integer())
    competition_type: Mapped[CompetitionType] = mapped_column(
        Enum(CompetitionType)
    )
    competition_format: Mapped[CompetitionFormat] = mapped_column(
        Enum(CompetitionFormat)
    )
    team_type: Mapped[TeamType] = mapped_column(Enum(TeamType))
    attribute_whitelist: ClassVar[list[str]] = [
        'name',
        'gender',
        'country',
        'tier',
        'competition_type',
        'competition_format',
        'team_type',
    ]

    @classmethod
    # TODO: Make this a Mixin
    def from_data(cls, data: Entity) -> Self:
        attributes = {
            attr: getattr(data, attr) for attr in cls.attribute_whitelist
        }
        return cls(**attributes)


class Season(Base):
    __tablename__ = 'season'

    id: Mapped[int] = mapped_column(primary_key=True)
    from_year: Mapped[int] = mapped_column(Integer())
    to_year: Mapped[int] = mapped_column(Integer())


class Fixture(Base):
    __tablename__ = 'fixture'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date())
    season_id: Mapped[int] = mapped_column(ForeignKey('season.id'))
    competition_id: Mapped[int] = mapped_column(ForeignKey('competition.id'))
    home_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    away_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    game_week: Mapped[int] = mapped_column(Integer())
    venue: Mapped[str] = mapped_column(String(30))

    season: Mapped['Season'] = relationship(foreign_keys=season_id)
    competition: Mapped['Competition'] = relationship(
        foreign_keys=competition_id
    )
    home_team: Mapped['TeamInstance'] = relationship(foreign_keys=home_team_id)
    away_team: Mapped['TeamInstance'] = relationship(foreign_keys=away_team_id)
