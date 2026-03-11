from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from .. import database as db

router = APIRouter(prefix="/api/events", tags=["events"])


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if "start_time" in doc:
        doc["start_time"] = doc["start_time"].isoformat()
    return doc


@router.get("")
async def list_events(
    sport: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    query: dict = {}
    if sport:
        query["sport"] = sport
    if status:
        query["status"] = status

    skip = (page - 1) * limit
    cursor = db.events().find(query).sort("start_time", -1).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    total = await db.events().count_documents(query)

    return {
        "items": [_serialize(d) for d in docs],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/{event_id}")
async def get_event(event_id: str):
    try:
        doc = await db.events().find_one({"_id": ObjectId(event_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if not doc:
        raise HTTPException(status_code=404, detail="Event not found")
    return _serialize(doc)
