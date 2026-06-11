#!/usr/bin/env bash
set -euo pipefail

: "${DROPLET_HOST:?Set DROPLET_HOST to the Droplet IPv4 address or domain.}"

SSH_USER="${SSH_USER:-root}"
APP_DIR="${APP_DIR:-/opt/worldcupiq}"
REPO_URL="${REPO_URL:-https://github.com/faww6z/worldcupiq.git}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_DB="${POSTGRES_DB:-worldcupiq}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-$(openssl rand -hex 24)}"
APP_DOMAIN="${APP_DOMAIN:-:80}"
PUBLIC_ORIGIN="${PUBLIC_ORIGIN:-http://${DROPLET_HOST}}"
VITE_API_BASE_URL="${VITE_API_BASE_URL:-/api}"

ssh "${SSH_USER}@${DROPLET_HOST}" /bin/bash <<REMOTE
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  apt-get update
  apt-get install -y ca-certificates curl git
  curl -fsSL https://get.docker.com | sh
fi

if ! docker compose version >/dev/null 2>&1; then
  apt-get update
  apt-get install -y docker-compose-plugin
fi

mkdir -p "${APP_DIR}"

if [ ! -d "${APP_DIR}/.git" ]; then
  git clone "${REPO_URL}" "${APP_DIR}"
else
  git -C "${APP_DIR}" pull --ff-only
fi

cd "${APP_DIR}"

cat > .env.production <<ENV
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}
DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
ENVIRONMENT=production
BACKEND_CORS_ORIGINS=${PUBLIC_ORIGIN}
VITE_API_BASE_URL=${VITE_API_BASE_URL}
APP_DOMAIN=${APP_DOMAIN}
HTTP_PORT=80
HTTPS_PORT=443
ENV

docker compose --env-file .env.production -f docker-compose.droplet.yml up --build -d
docker compose --env-file .env.production -f docker-compose.droplet.yml exec -T backend alembic upgrade head
docker compose --env-file .env.production -f docker-compose.droplet.yml exec -T backend python -m app.data_pipeline.seed_worldcup
docker compose --env-file .env.production -f docker-compose.droplet.yml ps
REMOTE

echo
echo "WorldCupIQ deployed:"
echo "  ${PUBLIC_ORIGIN}"
echo "  ${PUBLIC_ORIGIN}/api/health"
