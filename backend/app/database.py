from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client: AsyncIOMotorClient | None = None


def get_db():
    return client["statvault"]


def athletes():
    return get_db()["athletes"]


def teams():
    return get_db()["teams"]


def events():
    return get_db()["events"]


async def connect():
    global client
    client = AsyncIOMotorClient(settings.mongodb_uri)
    # Create indexes
    await athletes().create_index([("name", "text"), ("sport", 1)])
    await teams().create_index([("name", "text"), ("sport", 1)])
    await events().create_index([("sport", 1), ("status", 1), ("startTime", -1)])


async def disconnect():
    if client:
        client.close()
