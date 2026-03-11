from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from .. import database as db

router = APIRouter(prefix="/api/athletes", tags=["athletes"])


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if "team_id" in doc and not isinstance(doc["team_id"], str):
        doc["team_id"] = str(doc["team_id"])
    return doc


@router.get("")
async def list_athletes(
    sport: str | None = None,
    q: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    query: dict = {}
    if sport:
        query["sport"] = sport
    if q:
        query["$text"] = {"$search": q}

    skip = (page - 1) * limit
    cursor = db.athletes().find(query).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await db.athletes().count_documents(query)

    return {
        "items": [_serialize(d) for d in docs],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/{athlete_id}")
async def get_athlete(athlete_id: str):
    try:
        doc = await db.athletes().find_one({"_id": ObjectId(athlete_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if not doc:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return _serialize(doc)
