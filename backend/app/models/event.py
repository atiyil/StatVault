from pydantic import BaseModel, Field
from datetime import datetime


class TeamRef(BaseModel):
    id: str
    name: str


class Score(BaseModel):
    home: int
    away: int


class Event(BaseModel):
    id: str = Field(alias="_id")
    sport: str
    league: str
    home_team: TeamRef
    away_team: TeamRef
    start_time: datetime
    status: str  # upcoming | live | completed
    score: Score | None = None
    venue: str = ""

    model_config = {"populate_by_name": True}
