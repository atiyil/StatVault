# StatVault — Skills & Tech Stack Reference

Quick reference for every technology used in this project: what it is, why we use it, and links
to the most important docs. Consult this before asking Claude to explain a tool.

---

## Backend

### Python 3.12
- **Role:** Core API server, data ingestion, recommendation engine
- **Key features used:** `asyncio`, type hints, `match` statements, `tomllib`
- Docs: https://docs.python.org/3.12/

### FastAPI
- **Role:** HTTP API framework
- **Why:** Async-native, Pydantic integration, auto OpenAPI docs, high performance
- **Key concepts:** `APIRouter`, `Depends()`, lifespan context, `HTTPException`, `BackgroundTasks`
- Docs: https://fastapi.tiangolo.com/

### Pydantic v2
- **Role:** Data validation and serialization for all API models
- **Why:** Integrated with FastAPI, fast, strict type enforcement
- **Key concepts:** `BaseModel`, `model_validator`, `Field`, `ConfigDict`, `model_dump()`
- Docs: https://docs.pydantic.dev/latest/

### Motor
- **Role:** Async MongoDB driver for Python
- **Why:** Native asyncio support — required for use with FastAPI
- **Key concepts:** `AsyncIOMotorClient`, `AsyncIOMotorCollection`, `find()`, `find_one()`,
  `update_one()` with `upsert=True`, `aggregate()`
- Docs: https://motor.readthedocs.io/

### pydantic-settings
- **Role:** Environment variable management
- **Why:** Type-safe config with `.env` file support, integrates with Pydantic
- Docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

### pytest + pytest-asyncio
- **Role:** Testing framework for backend
- **Key concepts:** `@pytest.mark.asyncio`, `AsyncClient` from `httpx` for integration tests
- Docs: https://docs.pytest.org/ · https://pytest-asyncio.readthedocs.io/

---

## Gateway

### Node.js 20 (LTS)
- **Role:** Gateway service runtime
- **Key features used:** ESM modules, native `fetch`, `AbortController`
- Docs: https://nodejs.org/docs/latest-v20.x/api/

### TypeScript 5
- **Role:** Type-safe JavaScript for the gateway
- **Config:** `strict: true`, `noUncheckedIndexedAccess: true`
- Docs: https://www.typescriptlang.org/docs/

### Express 4
- **Role:** HTTP server framework for the gateway
- **Why:** Mature, minimal, compatible with Apollo Server's Express integration
- Docs: https://expressjs.com/

### Apollo Server v4
- **Role:** GraphQL server
- **Why:** Industry standard, excellent subscription support, integrates with Express
- **Key concepts:** `ApolloServer`, `expressMiddleware`, `makeExecutableSchema`,
  `GraphQLResolveInfo`, context function
- Docs: https://www.apollographql.com/docs/apollo-server/

### graphql-ws
- **Role:** WebSocket subscriptions transport
- **Why:** Replaces deprecated `subscriptions-transport-ws`, actively maintained
- **Key concepts:** `useServer()`, `PubSub`, `withFilter()`
- Docs: https://github.com/enisdenjo/graphql-ws

### DataLoader
- **Role:** Batch and cache DB lookups to prevent N+1 queries in GraphQL resolvers
- **Key concepts:** batch function, per-request instantiation, `load()`, `loadMany()`
- Docs: https://github.com/graphql/dataloader

### Zod
- **Role:** Runtime schema validation for webhook payloads and config
- **Key concepts:** `z.object()`, `z.parse()`, `z.safeParse()`, `infer<typeof schema>`
- Docs: https://zod.dev/

### Jest
- **Role:** Testing framework for gateway
- Docs: https://jestjs.io/

---

## Frontend

### Vue 3
- **Role:** Web UI framework
- **Syntax:** Composition API with `<script setup>` only — no Options API
- **Key concepts:** `ref`, `computed`, `watch`, `provide/inject`, `defineProps`, `defineEmits`
- Docs: https://vuejs.org/guide/

### Vite
- **Role:** Frontend build tool and dev server
- **Key concepts:** `vite.config.ts`, environment variables via `import.meta.env`, proxy config
- Docs: https://vitejs.dev/

### Vue Router 4
- **Role:** Client-side routing
- **Key concepts:** `createRouter`, `createWebHistory`, `useRoute`, `useRouter`,
  lazy-loaded routes with `() => import(...)`
- Docs: https://router.vuejs.org/

### Pinia
- **Role:** State management
- **Why:** Vue 3 native, simpler than Vuex, excellent TypeScript support
- **Key concepts:** `defineStore`, `storeToRefs`, composable-style stores
- Docs: https://pinia.vuejs.org/

### Apollo Client (Vue)
- **Role:** GraphQL client for Vue
- **Package:** `@apollo/client` + `@vue/apollo-composable`
- **Key concepts:** `useQuery`, `useMutation`, `useSubscription`, `InMemoryCache`,
  `ApolloClient`, WebSocket link for subscriptions
- Docs: https://v4.apollo.vuejs.org/

### TailwindCSS v3
- **Role:** Utility-first CSS
- **Key concepts:** `tailwind.config.ts`, `@apply` (sparingly), JIT mode (default in v3)
- Docs: https://tailwindcss.com/docs/

### graphql-codegen
- **Role:** Generate TypeScript types from GraphQL schema
- **Config:** `codegen.ts` at frontend root, generates to `src/types/graphql.ts`
- Docs: https://the-guild.dev/graphql/codegen

---

## Mobile

### React Native (Expo)
- **Role:** Cross-platform mobile app (iOS + Android)
- **Workflow:** Expo managed workflow
- **Key concepts:** `View`, `FlatList`, `StyleSheet`, `Platform`, hooks-based components
- Docs: https://reactnative.dev/docs/ · https://docs.expo.dev/

### Expo Router
- **Role:** File-based routing for React Native (like Next.js but mobile)
- **Key concepts:** `_layout.tsx`, `(tabs)/`, `(auth)/`, `useLocalSearchParams`
- Docs: https://expo.github.io/router/

### React Navigation v6
- **Role:** Navigation (used alongside Expo Router for complex flows)
- Docs: https://reactnavigation.org/docs/

### Zustand
- **Role:** Lightweight state management for mobile
- **Why:** Simpler than Redux, no boilerplate, works well with React Native
- Docs: https://zustand-demo.pmnd.rs/

### expo-secure-store
- **Role:** Secure JWT storage on device (encrypted keychain/keystore)
- **Why:** Never store tokens in `AsyncStorage` (plain text)
- Docs: https://docs.expo.dev/versions/latest/sdk/securestore/

---

## Infrastructure

### AWS CDK v2 (Python)
- **Role:** Infrastructure as code
- **Why:** CDK in Python keeps infra consistent with backend language
- **Key concepts:** `Stack`, `Construct`, `App`, `CfnOutput`, `RemovalPolicy`
- Docs: https://docs.aws.amazon.com/cdk/v2/guide/

### AWS Lambda
- **Role:** Scheduled data ingestion (TheSportsDB, ESPN), event processing
- **Runtime:** Python 3.12
- **Key concepts:** `handler(event, context)`, `aws_lambda_python_alpha` CDK construct for bundling
- Docs: https://docs.aws.amazon.com/lambda/

### AWS SQS
- **Role:** Decoupled message queue between Lambda ingestion and MongoDB write service
- **Key concepts:** Standard queue, visibility timeout, dead-letter queue (DLQ), batch processing
- Docs: https://docs.aws.amazon.com/sqs/

### AWS S3
- **Role:** Raw API response archive + athlete/team media assets
- **Key concepts:** Versioning, lifecycle policies, pre-signed URLs for direct media upload
- Docs: https://docs.aws.amazon.com/s3/

### AWS ECS (Fargate)
- **Role:** Container hosting for backend and gateway services
- **Key concepts:** Task definitions, services, ALB target groups, CloudMap for service discovery
- Docs: https://docs.aws.amazon.com/ecs/

### AWS SNS
- **Role:** Push notifications to mobile devices
- **Key concepts:** Platform application, endpoint ARN, `publish()` to endpoint
- Docs: https://docs.aws.amazon.com/sns/

### MongoDB Atlas
- **Role:** Cloud-hosted MongoDB (free M0 tier for dev/demo)
- **Key concepts:** Connection string, IP allowlist, indexes via Atlas UI or code
- Docs: https://www.mongodb.com/docs/atlas/

---

## External APIs

### TheSportsDB (free tier)
- **Base URL:** `https://www.thesportsdb.com/api/v1/json/3/`
- **Key endpoints:**
  - `searchteams.php?t={name}` — search teams
  - `searchplayers.php?p={name}` — search athletes
  - `eventsseason.php?id={league_id}&s={season}` — season schedule
  - `eventsnextleague.php?id={league_id}` — next events
- Docs: https://www.thesportsdb.com/api.php
- **Rate limit:** Free tier = API key "3", limited RPS — use caching

### ESPN (unofficial public API)
- **Base URL:** `https://site.api.espn.com/apis/site/v2/sports/`
- **Key endpoints:**
  - `football/nfl/scoreboard` — current NFL scores
  - `basketball/nba/scoreboard` — current NBA scores
  - `soccer/eng.1/scoreboard` — Premier League scores
- No API key required for public endpoints
- **Note:** Unofficial API — no SLA, structure may change

### SportsData.io (free tier)
- Requires account + API key
- Good for historical stats and detailed player data
- Docs: https://sportsdata.io/developers/api-documentation

---

## Dev Tools

### Docker + Docker Compose
- Local development: MongoDB + backend + gateway in containers
- `docker-compose.yml` at project root
- Do not use `docker-compose down -v` — it destroys the local DB volume

### GitHub Actions
- CI on push and PR: lint, type check, unit tests for all services
- Config: `.github/workflows/ci.yml`

### k6
- Load testing for performance benchmarking
- Target: `GET /api/feed` < 200ms p95 under 50 concurrent users
- Scripts in `scripts/load-test/`

### gitleaks
- Secret scanning in CI — fails build on committed secrets
- Config: `.gitleaks.toml`
