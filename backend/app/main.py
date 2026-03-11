from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import database as db
from .config import settings
from .routes import athletes, teams, events, feed


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    if settings.seed_on_startup:
        from .seed import seed_if_empty
        await seed_if_empty()
    yield
    await db.disconnect()


app = FastAPI(title="StatVault API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(athletes.router)
app.include_router(teams.router)
app.include_router(events.router)
app.include_router(feed.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
