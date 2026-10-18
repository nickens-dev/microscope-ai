from fastapi import FastAPI

from app.schemas import CreateGameInput

app = FastAPI(
    title="Microscope AI API",
    version="1.0.0"
)

@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("api/games")
def create_game(game: CreateGameInput):
    return game