# DigitalOcean Droplet Deployment

This is the first live-deploy path for the WorldCupIQ MVP. It uses one Droplet running Docker Compose:

- Caddy reverse proxy on ports 80/443.
- Nginx static frontend behind Caddy.
- FastAPI backend behind Caddy at `/api`.
- PostgreSQL inside the Docker network with no public database port.

## Recommended First Droplet

- Image: Ubuntu 24.04 LTS
- Size: `s-1vcpu-2gb`
- Region: nearest to you or your expected demo audience
- Authentication: SSH key
- Monitoring: enabled
- Backups: optional for the MVP, recommended before sharing widely

## Option A: Create Droplet in the DigitalOcean UI

1. Create a new Droplet.
2. Choose Ubuntu 24.04 LTS.
3. Choose a small Basic plan. Start with 1 vCPU / 2GB RAM.
4. Add your SSH key.
5. Enable monitoring.
6. Copy the Droplet public IPv4 address.
7. Deploy from your local machine:

```bash
DROPLET_HOST=your-droplet-ip ./scripts/deploy_droplet.sh
```

Then open:

```text
http://your-droplet-ip
http://your-droplet-ip/api/health
```

## Option B: Create Droplet with doctl

Install and authenticate `doctl` first:

```bash
brew install doctl
doctl auth init
```

Find your SSH key ID or fingerprint:

```bash
doctl compute ssh-key list
```

Create the Droplet:

```bash
DO_SSH_KEY_ID=your-key-id ./scripts/create_digitalocean_droplet.sh
```

Copy the returned public IPv4 address, then deploy:

```bash
DROPLET_HOST=your-droplet-ip ./scripts/deploy_droplet.sh
```

## Domain Setup Later

If you add a domain, point an `A` record at the Droplet IPv4 address and deploy with:

```bash
DROPLET_HOST=your-domain.com \
APP_DOMAIN=your-domain.com \
PUBLIC_ORIGIN=https://your-domain.com \
./scripts/deploy_droplet.sh
```

Caddy will automatically request and renew HTTPS certificates for valid public domains.

## Useful Operations

SSH into the Droplet:

```bash
ssh root@your-droplet-ip
```

Check containers:

```bash
cd /opt/worldcupiq
docker compose --env-file .env.production -f docker-compose.droplet.yml ps
```

View logs:

```bash
docker compose --env-file .env.production -f docker-compose.droplet.yml logs -f backend
docker compose --env-file .env.production -f docker-compose.droplet.yml logs -f caddy
```

Deploy the latest GitHub `main`:

```bash
DROPLET_HOST=your-droplet-ip ./scripts/deploy_droplet.sh
```

## Notes

- The deploy script creates `/opt/worldcupiq/.env.production` on the Droplet.
- Do not commit `.env.production`.
- The generated PostgreSQL password is persisted in that server-side env file.
- The database volume is named `worldcupiq_droplet_pgdata`.
