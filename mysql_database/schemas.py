from datetime import date

from sqlalchemy import String, Date, ForeignKey, Integer
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from mysql_database.enums import Position, TeamType, CompetitionType, CompetitionFormat


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date_of_birth: Mapped[date] = mapped_column(Date())
    country: Mapped[str] = mapped_column(String(30))

    player_instances: Mapped[list['PlayerInstance']] = relationship(
        back_populates='player', cascade='all, delete-orphan'
    )


class PlayerInstance(Base):
    __tablename__ = 'player_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('player.id'))
    team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))
    position: Mapped[Position] = mapped_column(ENUM(*Position.list()))

    player: Mapped['Player'] = relationship(back_populates='player_instances')
    team: Mapped['TeamInstance'] = relationship(back_populates='players')


class Team(Base):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    type: Mapped[TeamType] = mapped_column(ENUM(*TeamType.list()))
    year_founded: Mapped[int] = mapped_column(Integer())

    team_instances: Mapped[list['TeamInstance']] = relationship(back_populates='team')


class TeamInstance(Base):
    __tablename__ = 'team_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))

    team: Mapped['Team'] = relationship(back_populates='team_instances')
    players: Mapped[list['PlayerInstance']] = relationship(back_populates='team')


class Competition(Base):
    __tablename__ = 'competition'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    competition_type: Mapped[CompetitionType] = mapped_column(ENUM(*CompetitionType.list()))
    competition_format: Mapped[CompetitionFormat] = mapped_column(ENUM(*CompetitionFormat.list()))
    team_type: Mapped[TeamType] = mapped_column(ENUM(*TeamType.list()))


class Season(Base):
    __tablename__ = 'season'

    id: Mapped[int] = mapped_column(primary_key=True)
    from_year: Mapped[int] = mapped_column(Integer())
    to_year: Mapped[int] = mapped_column(Integer())


class Venue(Base):
    __tablename__ = 'venue'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    area: Mapped[str] = mapped_column(String(30), nullable=True)
    street: Mapped[str] = mapped_column(String(30))
    post_code: Mapped[str] = mapped_column(String(10))


class Fixture(Base):
    __tablename__ = 'fixture'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date())
    season_id: Mapped[int] = mapped_column(ForeignKey('season.id'))
    competition_id: Mapped[int] = mapped_column(ForeignKey('competition.id'))
    home_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    away_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    game_week: Mapped[int] = mapped_column(Integer())
    venue_id: Mapped[int] = mapped_column(ForeignKey('venue.id'))

    season: Mapped['Season'] = relationship()
    competition: Mapped['Competition'] = relationship()
    home_team: Mapped['TeamInstance'] = relationship(foreign_keys=home_team_id)
    away_team: Mapped['TeamInstance'] = relationship(foreign_keys=away_team_id)
    venue: Mapped['Venue'] = relationship()
