# StatVault — Claude Instructions

StatVault is a sports stats aggregator and social platform. This file tells Claude how to work
in this codebase. Read it before making any changes.

---

## Project Layout

```
StatVault/
├── backend/          # Python / FastAPI — core API, ingestion, recommendations
├── gateway/          # Node.js / Express + Apollo — GraphQL, WebSocket, webhooks
├── frontend/         # Vue 3 + Vite — web dashboard
├── mobile/           # React Native + Expo — mobile app
├── infra/            # AWS CDK (Python) — Lambda, SQS, S3, ECS
├── scripts/          # Seed data, migration, utility scripts
├── PROJECT_PLAN.md   # Architecture overview and phase goals
├── TASKS.md          # Task checklist — update as work progresses
└── SKILLS.md         # Tech stack reference
```

---

## Development Philosophy

- **Simplicity first.** Do not add abstractions until they are needed by at least two callers.
- **No over-engineering.** Every file, class, and function should have a clear, immediate purpose.
- **Stay in scope.** Only implement what the current task requires. Do not refactor adjacent code.
- **No placeholder code.** Do not write `TODO`, `pass`, or stub functions unless explicitly asked.
- **Fail loudly.** Prefer exceptions and early returns over silent failures or defensive fallbacks.

---

## Backend (Python / FastAPI)

### Conventions
- Python 3.12+. Use `pyproject.toml` for dependency management (no `setup.py`).
- Async everywhere: use `async def` for all route handlers and service functions.
- MongoDB via `motor` (async). Never use `pymongo` directly in route handlers.
- Pydantic v2 for all request/response models and data validation.
- Use `annotated-types` and `Annotated` for field constraints, not validators.
- No global state. Dependency-inject the DB client via FastAPI's `Depends()`.
- All IDs are `str` (MongoDB ObjectId stringified) in API responses, never raw `ObjectId`.

### Structure
```
backend/
├── app/
│   ├── main.py           # FastAPI app factory
│   ├── config.py         # Settings via pydantic-settings
│   ├── database.py       # Motor client, collection accessors
│   ├── models/           # Pydantic schemas (request + response)
│   ├── routes/           # One file per resource (athletes.py, teams.py, etc.)
│   ├── services/         # Business logic, one file per domain
│   └── middleware/       # Auth, logging, error handling
├── tests/
├── pyproject.toml
└── Dockerfile
```

### Patterns
- Routes: thin. Validate input, call service, return response. No business logic in routes.
- Services: stateless functions that accept data and a db client. No class-based services.
- Error handling: raise `HTTPException` from services. Use a global exception handler for
  unexpected errors — never return 500 with a stack trace in production.
- Pagination: cursor-based for feeds, offset-based for search. Use `limit` max of 100.

### Testing
- `pytest` + `pytest-asyncio`. Use `motor`'s test client or `mongomock-motor` for unit tests.
- Test file naming: `test_<module>.py` in `tests/`.
- At minimum: one happy-path and one error-path test per endpoint.

---

## Gateway (Node.js / Express + Apollo)

### Conventions
- Node 20+, TypeScript strict mode, ESM modules (`"type": "module"` in package.json).
- Use `@apollo/server` (v4) with Express integration. Do not use Apollo Studio cloud.
- Zod for runtime validation of webhook payloads. Do not use `any` types.
- All async functions must handle errors — no unhandled promise rejections.
- Use `graphql-ws` for WebSocket subscriptions. Do not use the deprecated
  `subscriptions-transport-ws`.

### Structure
```
gateway/
├── src/
│   ├── index.ts          # App entrypoint, server startup
│   ├── config.ts         # Env config with Zod validation
│   ├── schema/           # GraphQL type definitions (SDL files + resolvers)
│   │   ├── typeDefs.ts
│   │   └── resolvers/    # One file per type (athlete.ts, team.ts, etc.)
│   ├── dataloaders/      # DataLoader instances (one per resource)
│   ├── webhooks/         # Webhook handlers and signature verification
│   └── middleware/       # Auth, logging
├── tests/
├── package.json
└── Dockerfile
```

### Patterns
- Resolvers: call the Python backend via HTTP (or shared MongoDB client for performance).
  The gateway is the GraphQL surface — not a second data layer.
- DataLoaders: required for any resolver that could cause N+1 queries. One DataLoader
  per collection access pattern.
- Subscriptions: publish to an in-memory PubSub for dev; Redis PubSub adapter for prod.
- Context: always include `{ user, dataloaders }` — never pass raw request objects into resolvers.

### Testing
- Jest + `graphql-tag` for resolver tests. Mock the backend HTTP calls with `msw`.
- Test the full GraphQL operation (query/mutation/subscription), not individual resolver functions.

---

## Frontend (Vue 3)

### Conventions
- Vue 3 with `<script setup>` syntax only. No Options API.
- Pinia for state (auth store, feed store). No Vuex.
- TailwindCSS for styling. No scoped CSS unless absolutely necessary for component isolation.
- Apollo Client for GraphQL queries/mutations/subscriptions.
- Axios for direct REST calls (auth endpoints, file uploads).
- Vue Router with lazy-loaded routes (no eager imports of page components).

### Structure
```
frontend/
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/index.ts
│   ├── stores/           # Pinia stores
│   ├── views/            # Page-level components (one per route)
│   ├── components/       # Reusable UI components
│   ├── composables/      # Shared composition functions
│   ├── graphql/          # .graphql files or gql`` tagged queries
│   └── types/            # TypeScript interfaces (generated from GraphQL schema where possible)
├── index.html
├── vite.config.ts
└── tailwind.config.ts
```

### Patterns
- Use `useQuery`, `useMutation`, `useSubscription` from `@vue/apollo-composable`.
- Generate TypeScript types from the GraphQL schema using `graphql-codegen`. Do not hand-write
  types that can be generated.
- Infinite scroll: use `IntersectionObserver`, not scroll event listeners.
- Loading + error states: every async component must handle both — never leave the user
  looking at a blank screen.

---

## Mobile (React Native / Expo)

### Conventions
- Expo managed workflow. Do not eject unless there is no alternative.
- React Navigation v6 for all routing.
- Zustand for state management (lighter than Redux for mobile).
- Apollo Client (shared config with frontend where possible).
- `expo-secure-store` for JWT storage. Never use `AsyncStorage` for tokens.

### Structure
```
mobile/
├── app/
│   ├── _layout.tsx       # Root layout with navigation
│   ├── (auth)/           # Auth screens (Expo Router file-based routing)
│   └── (tabs)/           # Main tab screens
├── components/
├── hooks/
├── services/             # API clients
├── store/                # Zustand stores
└── app.json
```

---

## Infrastructure (AWS CDK)

### Conventions
- CDK v2 in Python. All constructs in `infra/stacks/`.
- One stack per environment concern: `NetworkStack`, `DataStack`, `ComputeStack`.
- Lambda functions live in `infra/lambdas/<function_name>/`. Each is a self-contained Python
  package with its own `requirements.txt`.
- Use `aws_lambda_python_alpha` for bundling Lambda dependencies.
- Tag all resources with `Project=StatVault` and `Environment=dev|prod`.
- No hardcoded ARNs or account IDs. Use SSM Parameter Store for cross-stack references.

---

## MongoDB

### Schema Rules
- All collections use `_id` as ObjectId (MongoDB default). API responses expose as string `id`.
- Use `createdAt` / `updatedAt` timestamps on all documents (set in service layer, not DB).
- Indexes must be defined in `backend/app/database.py` alongside the collection definition.
- Do not use `$lookup` (joins) in hot paths. Denormalize aggressively for read performance.
- Array fields (e.g., `follows[]`) must have a size cap. For unbounded data, use a separate
  collection (e.g., `follows` collection, not an embedded array on `users`).

### Collections Reference
See `PROJECT_PLAN.md` → Data Sources section for full schema definitions.

---

## Environment Variables

### Backend (`backend/.env`)
```
MONGODB_URI=mongodb://localhost:27017/statvault
JWT_SECRET=
AWS_REGION=us-east-1
AWS_SQS_QUEUE_URL=
THESPORTSDB_API_KEY=
ESPN_API_BASE_URL=https://site.api.espn.com/apis/site/v2
```

### Gateway (`gateway/.env`)
```
PORT=4000
BACKEND_URL=http://localhost:8000
MONGODB_URI=mongodb://localhost:27017/statvault
JWT_SECRET=
REDIS_URL=redis://localhost:6379
WEBHOOK_SECRET=
```

### Frontend (`frontend/.env`)
```
VITE_GRAPHQL_URL=http://localhost:4000/graphql
VITE_WS_URL=ws://localhost:4000/graphql
VITE_API_URL=http://localhost:8000
```

Never commit `.env` files. Always update `.env.example` when adding a new variable.

---

## Git Conventions

- Branch names: `feature/<name>`, `fix/<name>`, `chore/<name>`
- Commit messages: imperative mood, present tense. Example: `add athlete search endpoint`
- Do not commit commented-out code, debug prints, or `console.log` statements.
- Every PR should reference the TASKS.md item it completes.
- Mention AI tool usage in PR descriptions (e.g., "Scaffolded with Claude, refined manually").

---

## Running Locally

```bash
# Start all services
docker-compose up -d

# Backend (in backend/)
uvicorn app.main:app --reload --port 8000

# Gateway (in gateway/)
npm run dev   # starts on :4000

# Frontend (in frontend/)
npm run dev   # starts on :5173

# Mobile (in mobile/)
npx expo start
```

GraphQL playground: http://localhost:4000/graphql
FastAPI docs: http://localhost:8000/docs

---

## What Claude Should NOT Do

- Do not install packages without confirming with the user first.
- Do not modify `infra/` stacks without being explicitly asked — CDK changes can
  affect live AWS resources.
- Do not change MongoDB indexes on existing collections without flagging the migration impact.
- Do not run `docker-compose down -v` (destroys volumes with seed data).
- Do not push to `main` or create PRs autonomously.
- Do not generate or guess external API keys — prompt the user to provide them.
