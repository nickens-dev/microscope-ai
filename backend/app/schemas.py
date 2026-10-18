from enum import StrEnum
from pydantic import BaseModel, Field

class PlayerController(StrEnum):
    HUMAN = "human"
    AI = "ai"

class CreatePlayerInput(BaseModel):
    name: str = Field(min_length=1)
    controller: PlayerController
    persona_prompt: str | None = Field(
        default=None,
        alias="personaPrompt"
    )

    model_config = {
        "populate_by_name": True,
    }