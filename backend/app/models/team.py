from pydantic import BaseModel, Field


class RosterEntry(BaseModel):
    athlete_id: str
    name: str
    position: str


class Team(BaseModel):
    id: str = Field(alias="_id")
    name: str
    sport: str
    league: str
    city: str
    logo_url: str
    roster: list[RosterEntry] = []

    model_config = {"populate_by_name": True}
