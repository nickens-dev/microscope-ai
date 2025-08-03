from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.models.base import Base
from uuid import uuid4



class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)

    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=True)
    game = relationship("Game", foreign_keys=[game_id], post_update=True)

    cards = relationship("Card", secondary="tag_card_association", back_populates="tags")