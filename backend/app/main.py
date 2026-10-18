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

# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, status

from app.schemas import (
    CreateGameInput,
    GameResponse,
    GameStatus,
    PlayerResponse,
)

# ---------------------------------------------------------------------------
# API SETUP
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Microscope AI API",
    version="1.0.0"
)

# ---------------------------------------------------------------------------
# API HEALTH
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Return a basic API availability result.

    This endpoint verifies that the FastAPI process is running and can serve
    requests. It does not currently check a database or external dependency.
    """
    return {"status": "ok"}

# ---------------------------------------------------------------------------
# GAME MANAGEMENT API
# ---------------------------------------------------------------------------

@app.post(
    "/api/games",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_game(game: CreateGameInput) -> GameResponse:
    """Validate a game setup and construct its initial representation.

    Player seats are assigned in request order, beginning with seat 1. Game
    and player identifiers, initial status, and timestamps are owned by the
    server rather than accepted from the client.

    The returned game is not yet persisted.
    """
    now = datetime.now(timezone.utc)
    players = [
        PlayerResponse(
            id=uuid4(),
            seat=seat,
            name=player.name,
            controller=player.controller,
            persona_prompt=player.persona_prompt,
        )
        for seat, player, in enumerate(game.players, start=1)
    ]

    return GameResponse(
        id=uuid4(),
        title=game.title,
        status=GameStatus("setup"),
        bigPicture=game.big_picture,
        players=players,
        createdAt=now,
        updatedAt=now,
    )