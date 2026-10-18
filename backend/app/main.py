from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, status

from app.schemas import (
    CreateGameInput,
    GameResponse,
    GameStatus,
    PlayerResponse,
)

app = FastAPI(
    title="Microscope AI API",
    version="1.0.0"
)

@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.post(
    "/api/games",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_game(game: CreateGameInput) -> GameResponse:
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