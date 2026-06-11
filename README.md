# WorldCupIQ

WorldCupIQ is a World Cup 2026 prediction dashboard. The current MVP foundation is a local full-stack app that displays seeded World Cup fixtures from PostgreSQL through FastAPI and shows persisted Elo-style + Poisson match predictions, group tables, and predicted-result group impact in React.

## Current MVP

- FastAPI backend with SQLAlchemy models for groups, teams, and matches.
- PostgreSQL local development database through Docker Compose.
- Alembic migration for the first MVP tables.
- CSV seed data for groups, teams, and the full 72-match group-stage fixture list.
- React + TypeScript + Tailwind frontend with home and fixtures pages.
- Match Center page with predicted score, win/draw/loss probabilities, expected goals, top scorelines, current group table, simple group impact, and a short explanation.
- Persisted prediction outputs and model-run metadata for generated predictions.
- Backend tests for health, database setup, seed idempotency, match routes, prediction output, prediction persistence, group endpoints, and group-table sorting.
- GitHub Actions workflows for backend tests and frontend builds.

Historical international results, player data, Redis, Celery, monitoring, and deployment are intentionally deferred.

## MVP Status

This repository is currently a local MVP. It is ready to run with Docker Compose, but it has not yet been deployed to a public environment.

The prediction model is a seeded baseline: it combines hand-maintained Elo-style ratings, simple attack/defence strengths, a host adjustment, and a Poisson scoreline model. It is useful for demonstrating the product flow, but it is not yet trained or backtested on historical international match data.

## Local Setup

Copy the example environment if you want to override defaults:

```bash
cp .env.example .env
```

Start the full stack:

```bash
docker-compose up --build
```

In another terminal, run the migration and seed data:

```bash
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.data_pipeline.seed_worldcup
```

Open:

- Frontend: http://localhost:5173
- Backend health: http://localhost:8000/health
- Upcoming matches: http://localhost:8000/matches/upcoming
- First match prediction: http://localhost:8000/predictions/1
- Group A table: http://localhost:8000/groups/A/table

## Backend Tests

```bash
cd backend
python -m pytest
```

## Frontend Build

```bash
cd frontend
npm ci
npm run build
```

## Data Source

The fixture seed is a manually maintained full group-stage list based on FIFA's official World Cup 2026 schedule reference:

https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums

The source and verification date are recorded in `data/seed/fixtures_metadata.json`.

## Model Limitations

The current model is intentionally simple and transparent. See [docs/limitations.md](docs/limitations.md) for the full MVP caveats and the planned upgrades.

## Roadmap

1. Verify Docker Compose with PostgreSQL end-to-end.
2. Deploy the MVP with a production PostgreSQL database.
3. Add historical international results cleaning.
4. Replace seeded strengths with ratings built from cleaned historical matches.
5. Add official tiebreaker logic, best-third-place ranking, and knockout-stage simulation.
