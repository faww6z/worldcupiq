# Deployment Notes

WorldCupIQ is prepared for a Docker-based MVP deployment. The production image path differs from local development in two important ways:

- The backend runs Uvicorn without `--reload`.
- The frontend builds static assets and serves them through Nginx.
- The backend image includes `data/seed` so the seed script can run in production without a bind mount.

## Required Environment

Backend:

```text
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/worldcupiq
ENVIRONMENT=production
BACKEND_CORS_ORIGINS=https://YOUR_FRONTEND_DOMAIN
```

Frontend build:

```text
VITE_API_BASE_URL=https://YOUR_BACKEND_DOMAIN
```

Local production-like defaults are provided in `docker-compose.prod.yml`.

## Local Production-Like Smoke Test

From the repo root:

```bash
docker compose down
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
docker compose -f docker-compose.prod.yml exec backend python -m app.data_pipeline.seed_worldcup
```

Verify:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/matches/upcoming
```

Then open:

```text
http://localhost:5173
```

## DigitalOcean MVP Path

Preferred first deployment path:

1. Create a managed PostgreSQL database.
2. Build and deploy the backend Docker image.
3. Run Alembic migrations against the production database.
4. Run the seed script once against the production database.
5. Build and deploy the frontend with `VITE_API_BASE_URL` pointing to the backend URL.
6. Set `BACKEND_CORS_ORIGINS` to the frontend URL.
7. Verify `/health`, `/matches/upcoming`, `/predictions/1`, and the frontend match center.

For the one-Droplet path, use [docs/digitalocean.md](digitalocean.md). It runs Caddy in front of the frontend and backend, keeps PostgreSQL private to the Docker network, and exposes the API under `/api`.

## Release Checklist

- Backend image starts without `--reload`.
- Frontend image serves static files through Nginx.
- Production database has both Alembic revisions applied.
- Seed script imports 12 groups, 48 teams, and 72 matches.
- Frontend can reach the backend API from the deployed domain.
- GitHub Actions are green before deploy.
