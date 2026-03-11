from fastapi import APIRouter, HTTPException
from bson import ObjectId
from .. import database as db

router = APIRouter(prefix="/api/teams", tags=["teams"])


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    for entry in doc.get("roster", []):
        if "athlete_id" in entry and not isinstance(entry["athlete_id"], str):
            entry["athlete_id"] = str(entry["athlete_id"])
    return doc


@router.get("")
async def list_teams(sport: str | None = None, q: str | None = None):
    query: dict = {}
    if sport:
        query["sport"] = sport
    if q:
        query["$text"] = {"$search": q}

    docs = await db.teams().find(query).to_list(length=100)
    return [_serialize(d) for d in docs]


@router.get("/{team_id}")
async def get_team(team_id: str):
    try:
        doc = await db.teams().find_one({"_id": ObjectId(team_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if not doc:
        raise HTTPException(status_code=404, detail="Team not found")
    return _serialize(doc)
