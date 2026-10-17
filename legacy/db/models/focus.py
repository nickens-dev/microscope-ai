from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.models.base import Base
import uuid
from datetime import datetime, timezone

class Focus(Base):
    __tablename__ = "foci"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    turn = Column(Integer)

    author_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=True)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=True)

    author = relationship("Player", foreign_keys=[author_id], post_update=True)