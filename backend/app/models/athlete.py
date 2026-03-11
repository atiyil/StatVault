from pydantic import BaseModel, Field
from typing import Any


class Athlete(BaseModel):
    id: str = Field(alias="_id")
    name: str
    sport: str
    position: str
    team_id: str
    team_name: str
    nationality: str
    age: int
    stats: dict[str, Any]
    image_url: str

    model_config = {"populate_by_name": True}
