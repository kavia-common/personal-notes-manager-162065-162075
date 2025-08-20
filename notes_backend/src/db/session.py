from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase

from src.core.config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy Declarative Base."""
    pass


_engine = None
SessionLocal = None


# PUBLIC_INTERFACE
def get_engine():
    """Return SQLAlchemy engine, creating it if necessary."""
    global _engine
    if _engine is None:
        settings = get_settings()
        # Use psycopg (psycopg3) driver
        _engine = create_engine(settings.database_url, pool_pre_ping=True)
    return _engine


# PUBLIC_INTERFACE
def get_session_factory():
    """Return a configured session factory."""
    global SessionLocal
    if SessionLocal is None:
        engine = get_engine()
        SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return SessionLocal


# PUBLIC_INTERFACE
def init_db() -> None:
    """
    Initialize the database by creating tables if they do not exist.
    """
    from src.db import models  # noqa: F401 ensure models are imported
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
