# StatVault — Task List

Status legend: `[ ]` todo · `[~]` in progress · `[x]` done

---

## Phase 1 — Foundation

### Monorepo & Tooling
- [ ] Initialize git repo, add `.gitignore` (Python, Node, Expo, env files)
- [ ] Create top-level `README.md` with project overview and badges placeholder
- [ ] Create `docker-compose.yml` with MongoDB, backend, gateway services
- [ ] Add `.env.example` files for each service with required variable names
- [ ] Configure GitHub Actions: lint + unit test workflow on push to `main` and PRs

### Backend (Python / FastAPI)
- [ ] Scaffold `backend/` with `pyproject.toml` (or `requirements.txt`), `Makefile`
- [ ] Set up FastAPI app factory with lifespan, CORS, and exception handlers
- [ ] Configure MongoDB connection via `motor` (async driver)
- [ ] Define Pydantic models: `Athlete`, `Team`, `Event`, `User`
- [ ] Implement `GET /health` endpoint
- [ ] Add `pytest` setup with at least one passing test

### Gateway (Node.js / Express + Apollo)
- [ ] Scaffold `gateway/` with `package.json`, ESLint, Prettier config
- [ ] Set up Express app with Apollo Server (GraphQL) middleware
- [ ] Define initial GraphQL schema stubs (Query, Mutation, Subscription types)
- [ ] Configure WebSocket transport (graphql-ws or subscriptions-transport-ws)
- [ ] Implement `GET /health` endpoint
- [ ] Add Jest setup with at least one passing test

### MongoDB Schemas (collections)
- [ ] `users`: id, email, passwordHash, displayName, sports, follows, createdAt
- [ ] `athletes`: id, externalId, source, name, sport, team, position, stats, imageUrl
- [ ] `teams`: id, externalId, source, name, sport, league, logoUrl, roster[]
- [ ] `events`: id, externalId, source, sport, homeTeam, awayTeam, startTime, score, status
- [ ] `follows`: userId, entityType (athlete|team), entityId, createdAt
- [ ] `feed_items`: userId, entityType, entityId, eventType, payload, score, createdAt
- [ ] `interactions`: userId, itemId, type (view|click|save), createdAt

---

## Phase 2 — Data Ingestion Pipeline

### AWS Infrastructure
- [ ] Scaffold `infra/` with AWS CDK (Python), `cdk.json`, `app.py`
- [ ] Define SQS queue: `statsvault-ingestion-queue`
- [ ] Define S3 bucket: `statsvault-raw-data` (versioned, private)
- [ ] Define Lambda function: `ingest-thesportsdb` (Python, scheduled every 6h)
- [ ] Define Lambda function: `ingest-espn` (Python, scheduled every 5min for live)
- [ ] Define IAM roles with least-privilege permissions
- [ ] Add CDK deploy instructions to README

### TheSportsDB Ingestion (Lambda)
- [ ] Create `infra/lambdas/ingest_thesportsdb/` Python package
- [ ] Implement athlete fetch: search by sport, map to internal `Athlete` schema
- [ ] Implement team fetch: all teams per league, map to internal `Team` schema
- [ ] Implement event fetch: upcoming + recent events per league
- [ ] Store raw API response to S3 before normalization
- [ ] Publish normalized records to SQS ingestion queue
- [ ] Handle rate limiting with exponential backoff

### ESPN Ingestion (Lambda)
- [ ] Create `infra/lambdas/ingest_espn/` Python package
- [ ] Implement live scoreboard fetch (NFL, NBA, MLB, Soccer)
- [ ] Map ESPN event schema to internal `Event` schema
- [ ] Upsert events in MongoDB (idempotent by externalId + source)
- [ ] Publish score-change events to SQS for WebSocket fanout

### SQS Consumer (Backend)
- [ ] Add SQS consumer worker to FastAPI backend (background task or separate process)
- [ ] Consume ingestion queue: upsert athletes, teams, events into MongoDB
- [ ] Consume score-change events: update `events` collection, emit to WebSocket

### FastAPI Endpoints
- [ ] `GET /api/athletes?sport=&team=&q=&page=&limit=` — paginated athlete search
- [ ] `GET /api/athletes/{id}` — athlete detail with stats
- [ ] `GET /api/teams?sport=&league=&q=` — team search
- [ ] `GET /api/teams/{id}` — team detail with roster
- [ ] `GET /api/events?sport=&status=live|upcoming|completed&page=` — event list
- [ ] `GET /api/events/{id}` — event detail with live score

---

## Phase 3 — API Layer

### GraphQL (Gateway)
- [ ] Define full GraphQL schema: `Athlete`, `Team`, `Event`, `User`, `FeedItem`
- [ ] Implement resolvers: `query.athlete(id)`, `query.team(id)`, `query.event(id)`
- [ ] Implement resolver: `query.search(q, type)` — unified search
- [ ] Implement resolver: `query.feed(userId, cursor)` — paginated feed
- [ ] Implement resolver: `query.trending(sport, limit)` — trending entities
- [ ] Implement mutations: `follow(entityType, entityId)`, `unfollow(...)`
- [ ] Implement mutation: `updateProfile(displayName, sports)`
- [ ] Implement subscription: `liveScore(eventId)` — WebSocket score updates
- [ ] Add DataLoader for N+1 query prevention (batch athlete/team lookups)
- [ ] Add query depth + complexity limits

### Authentication
- [ ] JWT issuing endpoint: `POST /api/auth/register`, `POST /api/auth/login`
- [ ] JWT middleware in FastAPI (verify token on protected routes)
- [ ] JWT middleware in Gateway (pass decoded user to GraphQL context)
- [ ] Refresh token flow

### Webhooks
- [ ] `POST /webhooks/scores` — receive external score update payload
- [ ] HMAC-SHA256 signature verification middleware
- [ ] Parse payload, validate schema, publish to SQS score-change queue
- [ ] `POST /webhooks/events` — receive new event notifications
- [ ] Webhook registration endpoint (for demo): `POST /api/webhooks/register`
- [ ] Webhook delivery log (last 100 received, for debugging in demo)

---

## Phase 4 — Social Features

### Follow Graph
- [ ] `POST /api/follows` — follow an athlete or team
- [ ] `DELETE /api/follows/{entityType}/{entityId}` — unfollow
- [ ] `GET /api/follows` — list current user's follows
- [ ] `GET /api/athletes/{id}/followers/count` — follower count
- [ ] `GET /api/teams/{id}/followers/count` — follower count
- [ ] GraphQL mutation wrappers for follow/unfollow

### Personalized Feed
- [ ] Feed generation service: query `follows` → fetch recent `events` and activity for each entity
- [ ] Feed item scoring: recency decay + entity popularity boost
- [ ] `GET /api/feed?cursor=&limit=` — paginated personalized feed (REST)
- [ ] GraphQL `query.feed(cursor)` — same, via gateway
- [ ] Feed item types: `GAME_RESULT`, `GAME_UPCOMING`, `ATHLETE_STAT`, `TEAM_NEWS`
- [ ] Feed caching: cache per-user feed for 60 seconds (Redis or in-memory)

### Activity Timeline
- [ ] `GET /api/athletes/{id}/timeline` — recent events involving this athlete
- [ ] `GET /api/teams/{id}/timeline` — recent events for this team
- [ ] Timeline items sorted by date, limited to last 30

### Notifications
- [ ] AWS SNS topic: `statsvault-notifications`
- [ ] Device token registration endpoint: `POST /api/notifications/register`
- [ ] Trigger notification on: live game start (for followed teams), final score
- [ ] React Native: configure Expo push notifications, handle foreground/background

### Trending
- [ ] Background job (runs every 15min): compute trending score per entity
  - Trending score = follow_delta_24h * 2 + event_activity_24h
- [ ] Store trending rankings in MongoDB `trending` collection
- [ ] `GET /api/trending?sport=&limit=10` endpoint

---

## Phase 5 — Recommendation Engine

### Data Collection
- [ ] Track `interactions` events: view athlete profile, click feed item, save event
- [ ] `POST /api/interactions` endpoint (fire-and-forget, async)
- [ ] Build user interest vector from follows + interactions (sport, position, league weights)

### Collaborative Filtering
- [ ] Offline job (Lambda, runs daily): compute user-user similarity from follow graph
- [ ] "Users who follow X also follow Y" — store top-N similar athletes per athlete
- [ ] Store similarity scores in `athlete_similarities` collection

### Content-Based Filtering
- [ ] Athlete feature vector: sport (one-hot), league, position, nationality
- [ ] Cosine similarity between user interest vector and athlete feature vectors
- [ ] Store top-N recommendations per user in `user_recommendations` collection

### Recommendation API
- [ ] `GET /api/recommendations/athletes?limit=10` — personalized athlete suggestions
- [ ] `GET /api/recommendations/teams?limit=10` — personalized team suggestions
- [ ] Fallback for new users (cold start): return trending athletes in user's selected sports
- [ ] A/B flag: `rec_strategy=cf|content|trending` (query param, for demo)

### Tracking
- [ ] `POST /api/recommendations/{id}/impression` — record that rec was shown
- [ ] `POST /api/recommendations/{id}/click` — record click-through
- [ ] `GET /api/recommendations/stats` — CTR per strategy (demo analytics endpoint)

---

## Phase 6 — Frontend (Vue 3)

### Setup
- [ ] Scaffold `frontend/` with Vite + Vue 3 + TypeScript
- [ ] Configure Vue Router, Pinia (state management), TailwindCSS
- [ ] Configure Apollo Client for GraphQL
- [ ] Configure Axios for REST endpoints
- [ ] Set up auth store (JWT persist in localStorage)

### Pages & Components
- [ ] `AuthView` — login + register forms
- [ ] `ExploreView` — search bar, trending athletes/teams grid, sport filter tabs
- [ ] `FeedView` — personalized feed with infinite scroll, feed item cards
- [ ] `AthleteView` — profile header, stats table, timeline, follow button, recommendations sidebar
- [ ] `TeamView` — team info, roster list, recent results, follow button
- [ ] `LiveView` — live scoreboard (WebSocket), score tickers
- [ ] `SettingsView` — manage follows, notification preferences, account

### Components
- [ ] `AthleteCard` — compact card for grids (image, name, sport, follow toggle)
- [ ] `TeamCard` — compact card
- [ ] `FeedItem` — game result, upcoming game, stat highlight variants
- [ ] `ScoreTicker` — live score display with WebSocket subscription
- [ ] `RecommendationRail` — horizontal scroll of recommended athletes

---

## Phase 7 — Mobile (React Native)

### Setup
- [ ] Scaffold `mobile/` with Expo (managed workflow), TypeScript
- [ ] Configure React Navigation (stack + tab navigator)
- [ ] Configure Apollo Client (shared GraphQL schema)
- [ ] Auth flow using SecureStore for JWT

### Screens
- [ ] `LoginScreen`, `RegisterScreen`
- [ ] `HomeScreen` — feed + notification bell
- [ ] `LiveScreen` — live scores with auto-refresh via WebSocket
- [ ] `AthleteScreen` — profile, follow button
- [ ] `TeamScreen` — team profile, follow button
- [ ] `SearchScreen` — unified search
- [ ] Configure Expo push notifications + AWS SNS integration

---

## Phase 8 — Polish & Deploy

### Deployment
- [ ] Dockerize backend: `backend/Dockerfile`, multi-stage build
- [ ] Dockerize gateway: `gateway/Dockerfile`, multi-stage build
- [ ] ECS task definitions via CDK for backend + gateway
- [ ] Application Load Balancer (ALB) → ECS services
- [ ] MongoDB Atlas: provision free M0 cluster, update connection strings
- [ ] Vue frontend: `npm run build` → deploy to S3 + CloudFront CDN
- [ ] Custom domain + ACM certificate (HTTPS)
- [ ] Environment-specific configs: `dev`, `prod`

### Seed Data
- [ ] Write `scripts/seed.py`: populate 50+ athletes, 20+ teams, 100+ events from TheSportsDB
- [ ] Create 3 demo user accounts with pre-built follow graphs
- [ ] Seed interaction history to generate non-trivial recommendations

### Documentation
- [ ] Architecture diagram in README (ASCII or Mermaid)
- [ ] Demo GIF: feed, live scores, recommendation flow
- [ ] API reference: link to auto-generated FastAPI docs (`/docs`)
- [ ] GraphQL playground link
- [ ] Setup instructions: local dev + deploy
- [ ] Design decisions section (why each tech choice was made)

### Quality
- [ ] Backend: pytest coverage > 70% on core services
- [ ] Gateway: Jest coverage > 60% on resolvers
- [ ] Lighthouse score > 85 on Vue frontend
- [ ] All GitHub Actions green on main
- [ ] No secrets committed (gitleaks scan in CI)
- [ ] Response time < 200ms p95 for `/api/feed` (load test with k6)
