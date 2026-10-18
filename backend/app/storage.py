"""Temporary in-memory storage for application resources.

All stored data is lost whenever the backend process restarts.
"""

from uuid import UUID

from app.schemas import GameResponse

# ---------------------------------------------------------------------------
# MAPPINGS
# ---------------------------------------------------------------------------

# The dictionary maps game UUID -> complete GameResponse
game: dict[UUID, GameResponse] = {}