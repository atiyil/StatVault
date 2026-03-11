# StatVault — Project Plan

## Overview

StatVault is a sports stats aggregator and social platform that connects athletes, teams, and fans through real-time data, personalized feeds, and social interactions.

---

## Architecture

```
                        ┌─────────────────────────────┐
                        │        Clients               │
                        │  Vue SPA  │  React Native    │
                        └─────┬─────┴────────┬─────────┘
                              │              │
                        ┌─────▼──────────────▼─────────┐
                        │         API Gateway           │
                        │   Node.js / Express           │
                        │   REST + GraphQL + WebSocket  │
                        └─────┬────────────────┬────────┘
                              │                │
              ┌───────────────▼──┐      ┌──────▼──────────────┐
              │  Python Backend  │      │  Node.js Event Svc   │
              │  FastAPI         │      │  Webhooks / Live      │
              │  Data ingestion  │      │  Score updates        │
              └───────┬──────────┘      └──────┬───────────────┘
                      │                        │
              ┌───────▼────────────────────────▼───────┐
              │              MongoDB                    │
              │  athletes │ teams │ users │ events      │
              └───────────────────┬─────────────────────┘
                                  │
              ┌───────────────────▼─────────────────────┐
              │                  AWS                     │
              │  Lambda (scheduled ingestion)            │
              │  S3 (media assets)                       │
              │  EC2/ECS (service hosting)               │
              │  SQS (event queue)                       │
              └──────────────────────────────────────────┘
```

---

## Services

| Service | Tech | Responsibility |
|---|---|---|
| `backend/` | Python / FastAPI | Core REST API, data ingestion, recommendation engine |
| `gateway/` | Node.js / Express | GraphQL API, WebSocket, webhook receiver |
| `frontend/` | Vue 3 + Vite | Web dashboard — feeds, athlete profiles, search |
| `mobile/` | React Native + Expo | Mobile app — notifications, live scores |
| `infra/` | AWS CDK (Python) | Lambda, S3, SQS, ECS definitions |

---

## Data Sources (Public / Free Tier)

| API | Data | Integration |
|---|---|---|
| TheSportsDB | Athletes, teams, events, logos | REST polling via Lambda |
| ESPN Hidden API | Live scores, schedules | REST polling + webhook-style updates |
| SportsData.io (free) | Historical stats | REST, scheduled ingestion |

---

## Phases

### Phase 1 — Foundation (Week 1)
Goal: Monorepo scaffolded, databases running locally, CI skeleton.

- Monorepo structure with `backend/`, `gateway/`, `frontend/`, `mobile/`, `infra/`
- Docker Compose: MongoDB + backend + gateway
- Python FastAPI skeleton with health check
- Node.js Express/Apollo skeleton with health check
- MongoDB schemas: `users`, `athletes`, `teams`, `events`, `follows`, `feed_items`
- GitHub Actions CI (lint + test on push)
- `.env` strategy, secrets management pattern

### Phase 2 — Data Ingestion Pipeline (Week 2)
Goal: Real sports data flowing into MongoDB via AWS Lambda.

- AWS Lambda functions (Python) for scheduled API polling
- TheSportsDB ingestion: athletes, teams, league schedules
- ESPN ingestion: live scores, recent events
- SQS queue: decouple ingestion from DB writes
- S3: store raw API responses + athlete/team media assets
- FastAPI endpoints: `/athletes`, `/teams`, `/events` (paginated, filterable)
- Data normalization layer (map third-party schemas to internal models)

### Phase 3 — API Layer (Week 3)
Goal: Full REST + GraphQL + Webhook surface area exposed.

- GraphQL schema via Apollo Server (Node.js gateway)
- Queries: `athlete`, `team`, `event`, `feed`, `search`
- Mutations: `follow`, `unfollow`, `saveEvent`, `updateProfile`
- Subscriptions: live score updates via WebSocket
- Webhook endpoint: receive score/event updates from external providers
- Webhook signature verification + SQS fanout
- REST passthrough routes for clients that prefer REST

### Phase 4 — Social Features (Week 4)
Goal: Follow graph, activity feed, notifications.

- Follow/unfollow athletes and teams (stored as graph edges in MongoDB)
- Personalized feed: aggregate recent events from followed entities
- Feed ranking: recency + engagement score
- Activity timeline per athlete/team
- Push notifications: React Native + AWS SNS
- "Trending" athletes/teams: based on follow velocity + event activity

### Phase 5 — Recommendation Engine (Week 5)
Goal: "Athletes you might follow" — hits the explicit bonus qualification.

- User interest vector: built from follows + feed interaction events
- Athlete similarity: collaborative filtering (users who follow X also follow Y)
- Content-based: sport type, league, position similarity
- Recommendation API endpoint: `/recommendations/athletes`, `/recommendations/teams`
- A/B test flag: simple % split between CF and content-based results
- Exposure + click-through event tracking for future model improvement

### Phase 6 — Frontend (Vue) (Week 6)
Goal: Polished web dashboard.

- Auth: JWT login/register flow
- Explore page: search athletes/teams, trending section
- Feed page: personalized activity feed with infinite scroll
- Athlete profile page: stats, timeline, follow button
- Team profile page: roster, recent results, fan feed
- Settings: manage follows, notification preferences

### Phase 7 — Mobile (React Native) (Week 7)
Goal: Core mobile experience.

- Auth flow (shared JWT with web)
- Home feed (notifications + activity)
- Live scores screen (WebSocket)
- Athlete/team profile (read-only)
- Push notification integration (AWS SNS)

### Phase 8 — Polish + Deploy (Week 8)
Goal: Production-ready, publicly accessible, demo-ready.

- ECS deployment: backend + gateway as Docker containers
- CloudFront + S3: Vue frontend static hosting
- MongoDB Atlas: free tier cloud instance
- Custom domain + HTTPS
- README with architecture diagram, demo GIF, setup instructions
- Seed script: populate with 50+ real athletes/teams for demo
- Performance: response time < 200ms p95 for feed endpoint

---

## Key Technical Decisions

**Why FastAPI (not Flask/Django)?**
Async-native, auto-generated OpenAPI docs, Pydantic validation — best fit for a data-heavy ingestion service.

**Why Node.js for the gateway (not just Python)?**
Apollo Server (GraphQL) is the most mature JS GraphQL implementation. WebSocket handling and event-driven patterns are idiomatic in Node. Having both Python and Node.js also directly mirrors the job's dual-stack requirement.

**Why MongoDB (not Postgres)?**
Athlete/event data is document-shaped and schema-flexible. Social graph edges fit well as embedded arrays or a separate collection. Aligns with the job's explicit MongoDB requirement.

**Why AWS CDK in Python (not Terraform)?**
Keeps infra in Python, consistent with backend skillset. CDK is increasingly common in AWS-native shops.

**AI Tooling:**
Claude (claude-sonnet-4-6) used throughout for code generation, schema design, and debugging. Documented in commit messages and PR descriptions to demonstrate AI-augmented development velocity — a stated preference of the hiring team.

---

## Success Criteria (Interview Readiness)

- [ ] Live demo URL accessible
- [ ] GraphQL playground exposed
- [ ] Webhook endpoint documented + testable via curl
- [ ] Recommendation endpoint returns non-trivial results with seed data
- [ ] README covers architecture, setup, and design decisions
- [ ] < 5 second cold start for Lambda ingestion functions
- [ ] GitHub Actions green on main branch
