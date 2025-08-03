from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.models.base import Base
from uuid import uuid4
from datetime import datetime, timezone

class Legacy(Base):
    __tablename__ = "legacies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=True)
    reference_card_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=True)

    # relationships
    game = relationship("Game", foreign_keys=[game_id], post_update=True)
    author = relationship("Player", foreign_keys=[author_id], post_update=True)
    reference_card = relationship("Card", foreign_keys=[reference_card_id], post_update=True)