from db.db_session import SessionLocal
from db.models.card import Card
from uuid import UUID
from typing import List, Optional
from datetime import datetime, timezone

def create_card(game_id: UUID,
                card_type: str,
                summary: str,
                content: Optional[str] = None,
                parent_id: Optional[UUID] = None,
                period_id: Optional[UUID] = None,
                event_id: Optional[UUID] = None
            ) -> Card:
    db = SessionLocal()
    card = Card(
        game_id = game_id,
        type = card_type,
        summary = summary,
        content = content,
        parent_id = parent_id,
        period_id = period_id,
        event_id = event_id,
        created_at = datetime.now(timezone.utc),
        updated_at = datetime.now(timezone.utc)
    )

    last_position = db.query(Card).filter(
        Card.game_id == game_id, Card.type == card_type
    ).order_by(Card.position.desc()).first()

    card.position = (last_position.position + 1) if last_position else 0

    db.add(card)
    db.commit()
    db.refresh(card)
    db.close()
    return card

def get_cards_by_game_id(game_id: UUID) -> List[Card]:
    db = SessionLocal()
    cards = db.query(Card).filter(Card.game_id == game_id).all()
    db.close()
    return cards

def get_cards_by_type(game_id: UUID, card_type: str) -> List[Card]:
    db = SessionLocal()
    cards = db.query(Card).filter(Card.game_id == game_id, Card.card_type == card_type).all()
    db.close()
    return cards

def update_card(card_id: UUID, summary: Optional[str] = None, content: Optional[str] = None):
    db = SessionLocal()
    card = db.query(Card).get(card_id)
    if card:
        if summary:
            card.summary = summary
        if content:
            card.content = content
        card.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.close()

def delete_card(card_id: UUID):
    db = SessionLocal()
    card = db.query(Card).get(card_id)
    if card:
        db.delete(card)
        db.commit()
    db.close()