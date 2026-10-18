from enum import StrEnum
from pydantic import BaseModel, Field

class PlayerController(StrEnum):
    HUMAN = "human"
    AI = "ai"

class CreatePlayerInput(BaseModel):
    name: str = Field(min_length=1)
    controller: PlayerController
    persona_prompt: str | None = Field(
        min_length=1,
        alias="personaPrompt"
    )

    model_config = {
        "populate_by_name": True,
    }

class CreateGameInput(BaseModel):
    title: str = Field(min_length=1)
    big_picture: str = Field(
        default=None,
        alias="bigPicture"
    )
    players: list[CreatePlayerInput] = Field(
        min_length=2,
        max_length=5
    )

    model_config = {
        "populate_by_name": True,
    }