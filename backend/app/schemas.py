from enum import StrEnum
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, model_validator




class PlayerController(StrEnum):
    HUMAN = "human"
    AI = "ai"

class GameStatus(StrEnum):
    SETUP = "setup"
    ACTIVE = "active"
    COMPLETE = "complete"




class CreatePlayerInput(BaseModel):
    name: str = Field(min_length=1)
    controller: PlayerController
    persona_prompt: str | None = Field(
        default=None,
        min_length=1,
        alias="personaPrompt"
    )

    model_config = {
        "populate_by_name": True,
    }

    @model_validator(mode='after')
    def validate_persona_prompt(self):
        if self.controller == PlayerController.AI:
            if not self.persona_prompt or not self.persona_prompt.strip():
                raise ValueError("AI players must have a persona prompt.")
        if self.controller ==  PlayerController.HUMAN:
            if self.persona_prompt is not None:
                raise ValueError("Human players cannot have a persona prompt.")
        return self

class CreateGameInput(BaseModel):
    title: str = Field(min_length=1)
    big_picture: str = Field(
        alias="bigPicture"
    )
    players: list[CreatePlayerInput] = Field(
        min_length=2,
        max_length=5
    )

    model_config = {
        "populate_by_name": True,
    }



class PlayerResponse(BaseModel):
    id: UUID
    seat: int = Field(ge=1, le=5)
    name: str
    controller: PlayerController
    persona_prompt: str | None = Field(
        default=None,
        alias="personaPrompt"
    )

    model_config = {
        "populate_by_name": True,
    }

class GameResponse(BaseModel):
    id: UUID
    title: str
    status: GameStatus
    big_picture: str = Field(
        min_length=1,
        alias="bigPicture"
    )
    players: list[PlayerResponse]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = {
        "populate_by_name": True,
    }