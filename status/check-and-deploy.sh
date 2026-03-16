#!/usr/bin/env bash
# Daily portal status check + commit + deploy to CF Pages
set -euo pipefail

cd "$(dirname "$0")/.."

# Run the check
python3 status/check.py

# Commit if there are changes
if git diff --quiet status/data/; then
  echo "No changes to commit"
else
  git add status/data/
  DATE=$(date -u +%Y-%m-%d)
  git commit -m "status: daily check ${DATE}"
  git push
fi

# Deploy to CF Pages
CF_TOKEN=$(pass cloudflare/api-token)
CLOUDFLARE_API_TOKEN=$CF_TOKEN npx wrangler pages deploy status --project-name gov-portal-status --branch main
echo "✅ Deployed"
