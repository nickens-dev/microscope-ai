"""SQLAlchemy engine, session, and base-model configuration."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# ---------------------------------------------------------------------------
# DATABASE LOCATION
# ---------------------------------------------------------------------------

BACKEND_DIRECTORY = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = BACKEND_DIRECTORY / "data"
DATABASE_PATH = DATA_DIRECTORY / "microscope.db"

DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# ---------------------------------------------------------------------------
# SQLALCHEMY CONFIGURATION
# ---------------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class inherited by all SQLAlchemy database models."""


def get_database_session() -> Generator[Session, None, None]:
    """Provide one database session for the duration of an API request."""

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()