from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.models.base import Base

tag_card_association = Table(
    "tag_card_association",
    Base.metadata,
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
    Column("card_id", UUID(as_uuid=True), ForeignKey("cards.id"), primary_key=True)
)