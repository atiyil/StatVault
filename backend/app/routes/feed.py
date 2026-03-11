from fastapi import APIRouter, Query
from .. import database as db

router = APIRouter(prefix="/api", tags=["feed"])


def _serialize_event(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if "start_time" in doc:
        doc["start_time"] = doc["start_time"].isoformat()
    return doc


def _serialize_entity(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("/feed")
async def get_feed(limit: int = Query(20, ge=1, le=50)):
    """Recent events across all sports, newest first."""
    cursor = db.events().find({}).sort("start_time", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [_serialize_event(d) for d in docs]


@router.get("/trending")
async def get_trending(sport: str | None = None, limit: int = Query(10, ge=1, le=20)):
    """Return a mix of trending athletes and teams (static for demo)."""
    athlete_query: dict = {}
    team_query: dict = {}
    if sport:
        athlete_query["sport"] = sport
        team_query["sport"] = sport

    athletes = await db.athletes().find(athlete_query).limit(limit).to_list(length=limit)
    teams_list = await db.teams().find(team_query).limit(limit // 2).to_list(length=limit // 2)

    return {
        "athletes": [_serialize_entity(a) for a in athletes],
        "teams": [_serialize_entity(t) for t in teams_list],
    }
