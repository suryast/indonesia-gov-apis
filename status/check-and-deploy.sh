#!/usr/bin/env bash
# Check only by default; deployment requires explicit --deploy and configuration.
set -euo pipefail
cd "$(dirname "$0")/.."

deploy=0
if [[ "${1:-}" == "--deploy" ]]; then
  deploy=1
  shift
  : "${STATUS_PAGES_PROJECT:?Set STATUS_PAGES_PROJECT for explicit deployment}"
  : "${CLOUDFLARE_API_TOKEN:?Provide CLOUDFLARE_API_TOKEN through your secret store}"
  command -v wrangler >/dev/null || { printf '%s\n' 'Install a reviewed Wrangler version first.' >&2; exit 1; }
  # Only repository observations may deploy; scratch checker outputs are check-only.
  for arg in "$@"; do
    case "$arg" in --output-dir|--output-dir=*) printf '%s\n' '--output-dir is check-only.' >&2; exit 1 ;; esac
  done
fi

python3 status/check.py "$@"
# No inline history generator, implicit git commit/push, token printing, or npx install.
if [[ "$deploy" == 1 ]]; then
  staging_parent="${TMPDIR:-${HOME}/.cache}"
  mkdir -p -- "$staging_parent"
  staging_root="$(mktemp -d "$staging_parent/gov-status-pages.XXXXXX")"
  trap 'rm -rf -- "$staging_root"' EXIT
  python3 scripts/check_repository.py --stage-static "$staging_root/site"
  wrangler pages deploy "$staging_root/site" --project-name "$STATUS_PAGES_PROJECT" --branch "${STATUS_PAGES_BRANCH:-main}"
fi
