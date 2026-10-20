"""SQLAlchemy database models for persisted Microscope games."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# ---------------------------------------------------------------------------
# UTILS
# ---------------------------------------------------------------------------

def utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""

    return datetime.now(timezone.utc)

# ---------------------------------------------------------------------------
# MODELS
# ---------------------------------------------------------------------------

class GameModel(Base):
    """Database representation of one Microscope game."""

    __tablename__ = "games"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    big_picture: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="setup",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    players: Mapped[list[PlayerModel]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
        order_by="PlayerModel.seat",
    )

class PlayerModel(Base):
    """Database representation of one ordered player seat."""

    __tablename__ = "players"

    __table_args__ = (
        UniqueConstraint(
            "game_id",
            "seat",
            name="uq_players_game_seat",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    game_id: Mapped[str] = mapped_column(
        ForeignKey("games.id"),
        nullable=False,
        index=True,
    )

    seat: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    controller: Mapped[str] = mapped_column(String(20), nullable=False)
    persona_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)

    game: Mapped[GameModel] = relationship(
        back_populates="players",
    )