# StatVault

A sports stats aggregator and social platform that connects athletes, teams, and fans through real-time data, personalized feeds, and social interactions.

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.12, FastAPI, Motor (MongoDB) |
| Frontend | Vue 3, Vite, TailwindCSS |
| Database | MongoDB 7 |

## Project Structure

```
StatVault/
├── backend/     # FastAPI REST API — athletes, teams, events, feed
├── frontend/    # Vue 3 web dashboard
├── docker-compose.yml
└── .env.example
```

## Quick Start (Docker)

```bash
docker compose up
```

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API docs**: http://localhost:8000/docs

Seed data (athletes, teams, events) is loaded automatically on first boot.

## Local Development (without Docker)

**Terminal 1 — MongoDB**
```bash
mongod
```

**Terminal 2 — Backend**
```bash
cd backend
pip install -r requirements.txt
SEED_ON_STARTUP=true uvicorn app.main:app --reload
```

**Terminal 3 — Frontend**
```bash
cd frontend
npm install && npm run dev
```

## API Endpoints

| Endpoint | Description |
|---------|-------------|
| `GET /health` | Health check |
| `GET /api/athletes` | List athletes (paginated, filterable by sport, search) |
| `GET /api/athletes/:id` | Get athlete by ID |
| `GET /api/teams` | List teams |
| `GET /api/teams/:id` | Get team by ID |
| `GET /api/events` | List events (filterable by sport, status) |
| `GET /api/events/:id` | Get event by ID |
| `GET /api/feed` | Recent events feed |
| `GET /api/trending` | Trending athletes and teams |

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed. See `.env.example` for all supported variables.

## License

MIT
