from db.db_session import SessionLocal
from db.models.game import Game
from uuid import UUID

def create_game(name: str) -> Game:
    db = SessionLocal()
    game = Game(name=name)
    db.add(game)
    db.commit()
    db.refresh(game)
    db.close()
    return game

def get_all_games() -> list[Game]:
    db = SessionLocal()
    games = db.query(Game).all()
    db.close()
    return games

def get_game_by_id(game_id: UUID) -> Game:
    db = SessionLocal()
    game = db.query(Game).get(game_id)
    db.close()
    return game

def delete_game_by_id(game_id: UUID):
    db = SessionLocal()
    game = db.query(Game).get(game_id)
    if game:
        db.delete(game)
        db.commit()
    db.close()