from contextlib import contextmanager, AbstractContextManager
from logging import getLogger
from typing import Callable

from sqlalchemy import URL, create_engine, Connection
from sqlalchemy.orm import scoped_session, sessionmaker, Session

logger = getLogger(__name__)

SessionFactory = Callable[..., AbstractContextManager[Session]]
ConnectionFactory = Callable[..., AbstractContextManager[Connection]]


class Database:
    def __init__(self, url_object: URL) -> None:
        self._engine = create_engine(url_object)
        self._session_factory = scoped_session(
            sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False
            )
        )

    @contextmanager
    def session(self) -> SessionFactory:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def connection(self) -> ConnectionFactory:
        connection: Connection = self._engine.connect()
        try:
            yield connection
        except Exception:
            logger.exception('Connection rollback because of exception')
            connection.rollback()
            raise
        finally:
            connection.close()
