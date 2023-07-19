from datetime import date

from sqlalchemy import String, Date, ForeignKey, Integer, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database.enums import Position, TeamType, CompetitionType, CompetitionFormat


class Base(DeclarativeBase):
    pass


class PlayerTable(Base):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date_of_birth: Mapped[date] = mapped_column(Date())
    country: Mapped[str] = mapped_column(String(30))

    player_instances: Mapped[list['PlayerInstanceTable']] = relationship(
        back_populates='player', cascade='all, delete-orphan'
    )


class PlayerInstanceTable(Base):
    __tablename__ = 'player_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('player.id'))
    team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))
    position: Mapped[Position] = mapped_column(Enum(Position))

    player: Mapped['PlayerTable'] = relationship(back_populates='player_instances')
    team: Mapped['TeamInstanceTable'] = relationship(back_populates='players')


class TeamTable(Base):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    type: Mapped[TeamType] = mapped_column(Enum(TeamType))
    year_founded: Mapped[int] = mapped_column(Integer())

    team_instances: Mapped[list['TeamInstanceTable']] = relationship(back_populates='team')


class TeamInstanceTable(Base):
    __tablename__ = 'team_instance'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    fixture_id: Mapped[int] = mapped_column(ForeignKey('fixture.id'))

    team: Mapped['TeamTable'] = relationship(back_populates='team_instances')
    players: Mapped[list['PlayerInstanceTable']] = relationship(back_populates='team')


class CompetitionTable(Base):
    __tablename__ = 'competition'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    competition_type: Mapped[CompetitionType] = mapped_column(Enum(CompetitionType))
    competition_format: Mapped[CompetitionFormat] = mapped_column(Enum(CompetitionFormat))
    team_type: Mapped[TeamType] = mapped_column(Enum(TeamType))


class SeasonTable(Base):
    __tablename__ = 'season'

    id: Mapped[int] = mapped_column(primary_key=True)
    from_year: Mapped[int] = mapped_column(Integer())
    to_year: Mapped[int] = mapped_column(Integer())


class VenueTable(Base):
    __tablename__ = 'venue'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    area: Mapped[str] = mapped_column(String(30), nullable=True)
    street: Mapped[str] = mapped_column(String(30))
    post_code: Mapped[str] = mapped_column(String(10), nullable=True)


class FixtureTable(Base):
    __tablename__ = 'fixture'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date())
    season_id: Mapped[int] = mapped_column(ForeignKey('season.id'))
    competition_id: Mapped[int] = mapped_column(ForeignKey('competition.id'))
    home_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    away_team_id: Mapped[int] = mapped_column(ForeignKey('team_instance.id'))
    game_week: Mapped[int] = mapped_column(Integer())
    venue_id: Mapped[int] = mapped_column(ForeignKey('venue.id'))

    season: Mapped['SeasonTable'] = relationship()
    competition: Mapped['CompetitionTable'] = relationship()
    home_team: Mapped['TeamInstanceTable'] = relationship(foreign_keys=home_team_id)
    away_team: Mapped['TeamInstanceTable'] = relationship(foreign_keys=away_team_id)
    venue: Mapped['VenueTable'] = relationship()
