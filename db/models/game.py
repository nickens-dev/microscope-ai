from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from db.models.base import Base
from uuid import uuid4
from datetime import datetime, timezone

class Game(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    big_picture = Column(String)
    palette_yes = Column(String)
    palette_no = Column(String)

    starting_period_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=True)
    ending_period_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=True)