"""Pydantic schemas used by the Microscope AI HTTP API.

Request schemas describe data clients are allowed to submit. Response schemas
describe data returned by the server, including server-owned identifiers,
seat assignments, status, and timestamps.

Python attributes use snake_case. JSON properties use camelCase aliases where
needed, such as ``big_picture`` becoming ``bigPicture``.
"""

from enum import StrEnum
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, model_validator

# ---------------------------------------------------------------------------
# ENUMERATIONS
# ---------------------------------------------------------------------------

class PlayerController(StrEnum):
    """Identify whether a seat is controlled by a human or an AI agent."""

    HUMAN = "human"
    AI = "ai"

class GameStatus(StrEnum):
    """Represent the current lifecycle phase of a game."""

    SETUP = "setup"
    ACTIVE = "active"
    COMPLETE = "complete"

# ---------------------------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------------------------

class CreatePlayerInput(BaseModel):
    """Describe one player seat supplied while creating a game.

    AI players require a meaningful persona prompt. Human players cannot have
    a persona prompt because their decisions are entered manually.
    """

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
        """Enforce persona-prompt rules for the selected controller type."""

        if self.controller == PlayerController.AI:
            if not self.persona_prompt or not self.persona_prompt.strip():
                raise ValueError("AI players must have a persona prompt.")
        if self.controller ==  PlayerController.HUMAN:
            if self.persona_prompt is not None:
                raise ValueError("Human players cannot have a persona prompt.")
        return self

class CreateGameInput(BaseModel):
    """Describe client-supplied data for creating a new game.

    A game requires a title, a big picture, and between two and five players.
    Player list order determines the initial seat order.
    """

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

# ---------------------------------------------------------------------------
# RESPONSE MODELS
# ---------------------------------------------------------------------------

class PlayerResponse(BaseModel):
    """Represent a player seat returned by the API.

    The server creates the player ID and assigns the seat number.
    """

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
        "from_attributes": True,
    }

class GameResponse(BaseModel):
    """Represent a game returned by the API.

    This model combines accepted setup data with server-owned identifiers,
    lifecycle status, ordered player seats, and timestamps.
    """

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
        "from_attributes": True,
    }