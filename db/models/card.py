from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4

from db.models.base import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String, nullable=False)

    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=True)

    summary = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    tone = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    # card ordering
    position = Column(Integer, nullable=True)

    # for scenes
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    dictated = Column(Boolean, default=False)

    # for definitions
    parent_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=True)
    period_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=True)

    # tags
    tags = relationship("Tag", secondary="tag_card_association", back_populates="cards")
