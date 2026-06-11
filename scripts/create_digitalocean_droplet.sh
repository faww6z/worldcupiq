#!/usr/bin/env bash
set -euo pipefail

: "${DO_SSH_KEY_ID:?Set DO_SSH_KEY_ID to a DigitalOcean SSH key ID or fingerprint.}"

DROPLET_NAME="${DROPLET_NAME:-worldcupiq-mvp}"
DROPLET_REGION="${DROPLET_REGION:-nyc3}"
DROPLET_SIZE="${DROPLET_SIZE:-s-1vcpu-2gb}"
DROPLET_IMAGE="${DROPLET_IMAGE:-ubuntu-24-04-x64}"

if ! command -v doctl >/dev/null 2>&1; then
  echo "doctl is not installed. Install it first, then run: doctl auth init"
  exit 1
fi

doctl compute droplet create "$DROPLET_NAME" \
  --region "$DROPLET_REGION" \
  --size "$DROPLET_SIZE" \
  --image "$DROPLET_IMAGE" \
  --ssh-keys "$DO_SSH_KEY_ID" \
  --tag-names worldcupiq,mvp \
  --enable-monitoring \
  --wait \
  --format ID,Name,PublicIPv4,Status \
  --no-header
