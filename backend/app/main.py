"""FastAPI application and HTTP route definitions for Microscope AI.

This module creates the FastAPI application and defines the public HTTP
endpoints exposed by the backend.

The route layer is currently responsible for:

- Reporting service health.
- Validating game-creation requests with Pydantic schemas.
- Assigning server-owned game and player values.
- Returning a documented response model.

Game data is not yet persisted. Creating a game currently constructs and
returns a response that exists only for the duration of the request.
"""

from uuid import UUID

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import Base, engine, get_database_session
from app.models import GameModel, PlayerModel
from app.schemas import (
    CreateGameInput,
    GameResponse,
    GameStatus,
    PlayerResponse,
)

# ---------------------------------------------------------------------------
# APPLICATION CONFIGURATION
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Microscope AI API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# HEALTH ROUTES
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Return a basic API availability result.

    This endpoint verifies that the FastAPI process is running and can serve
    requests. It does not currently check a database or external dependency.
    """
    return {"status": "ok"}

# ---------------------------------------------------------------------------
# GAME ROUTES
# ---------------------------------------------------------------------------

@app.post(
    "/api/games",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_game(
        game: CreateGameInput,
        session: Session = Depends(get_database_session),
) -> GameResponse:
    """Validate a game setup and construct its initial representation.

    Player seats are assigned in request order, beginning with seat 1. Game
    and player identifiers, initial status, and timestamps are owned by the
    server rather than accepted from the client.

    The returned game is not yet persisted.
    """
    created_game = GameModel(
        title=game.title,
        big_picture=game.big_picture,
        status=GameStatus.SETUP.value,
    )

    created_game.players = [
        PlayerModel(
            seat=seat,
            name=player.name,
            controller=player.controller.value,
            persona_prompt=player.persona_prompt,
        )
        for seat, player, in enumerate(game.players, start=1)
    ]

    session.add(created_game)
    session.commit()
    session.refresh(created_game)

    return GameResponse.model_validate(created_game)

@app.get(
    "/api/games/{game_id}",
    response_model=GameResponse,
)
def get_game(
        game_id: UUID,
        session: Session = Depends(get_database_session),
) -> GameResponse:
    """Return one game by its server-generated identifier."""
    statement = (
        select(GameModel)
        .options(selectinload(GameModel.players))
        .where(GameModel.id == str(game_id))
    )
    game = session.scalar(statement)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    return GameResponse.model_validate(game)