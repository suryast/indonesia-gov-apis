# Portal status monitor

Requires Python 3.10+, curl, and a Unix host (standard-library `fcntl` locking).
No Python dependencies. The registry in `check.py` selects **monitored public
endpoints**, not every catalog source. A successful HTTP check does not establish
API correctness, licensing, authorization, or the availability of authenticated
operations. No response bodies, raw errors, probe IPs, SSH targets or secrets are
published. `cmsbl-halal` is labeled as a legacy, unverified web endpoint, not a
certificate or business API. `ojk-sikepo` currently checks the OJK root only;
its display label explicitly says so, and it does not establish SIKEPO availability.
AHU labels avoid asserting a stale ministry ownership. Monitored IDs and URLs are
retained for historical continuity; catalog mappings should use IDs, not labels.

## October 10, 2026 PR10 integration

The registry includes the exact 18 PR10 additions and four repointed URLs from
`origin/main` (PR10, 0508c7b): **75 unique monitor IDs**. IDs retain their histories;
old snapshots and labels are not rewritten. `2026-10-10-update.md` is copied
unchanged as the upstream historical review note, not current validation evidence.
Its proposed US/Sydney geography is not adopted: local and CI geography remains
unknown unless explicitly configured. Its new URLs and EXPECT markers originated
in untested desk research; integration tests are not live endpoint validation.
A separate current 75-endpoint observation is required before publication.

EXPECT is an exact case-insensitive static substring heuristic. Only public root,
documentation and public data responses are inspected; no personal-data queries,
credentials or authenticated operations. Downloads have a hard **262144-byte**
cap via curl `--max-filesize` (curl >=8.4 required for unknown-length bodies), the
same per-request timeout, no decompression, and private temporary cleanup. Older
curl skips body collection. `content_check` is `matched`, `missing`, or `unverified`;
no body, raw error, extracted personal field or whole response is published.
Cap exits preserve `up` with `unverified`; transport failures retain their accurate
curl taxonomy with unverified content. Only successful complete bodies can be
`missing`/`degraded`; truncated bodies never prove marker absence. HTTPS redirects
cannot downgrade to HTTP. No source geography is inferred and no SSH is used.

## Run

```sh
# From the repository root; choose an output outside tracked status/data for trials.
python3 status/check.py --output-dir "$HOME/status-trial" --workers 4 --timeout 10 \
  --source-location 'Your verified region' --source-provider 'Your verified provider' \
  --source-type 'CI runner'
```

The source is `local`; its metadata defaults to **Not configured**, not an inferred
country/provider. Also configurable via `STATUS_SOURCE_LOCATION`,
`STATUS_SOURCE_PROVIDER`, `STATUS_SOURCE_TYPE`. These are public descriptive
labels: never put credentials, hostnames or personal information in them. The
checker does not geolocate the machine. Legacy `au`/`id` snapshots still render;
their recorded metadata is retained, not retroactively corrected.

The former private SSH probe was removed entirely. No remote probes are made,
and old `JAKARTA_*` variables no longer activate them. Any future remote source
needs an explicitly provisioned trusted transport and recorded source metadata.

Timeout is per endpoint (0 < seconds <= 120, default 10); workers are bounded
1–32 (default 4). curl configuration files are disabled, certificate verification
stays enabled, redirects are limited to three and HTTP(S) only. Normal environment
proxy configuration remains effective: the label must describe the actual probe
vantage point. One public GET per endpoint, plus redirects; no retries or payload
publication. Selected public bodies are held only in private temporary files for
bounded marker inspection, then removed on every exit. Same-output-directory concurrent runs fail rather than overwrite each
other. The checker reports only stable portal IDs/statuses, not raw stderr.

## Status meanings

- `up`: HTTP 200–399 with no curl transport failure, or HTTP reachability established
  when a content download reaches its byte cap (curl exit 63).
- `degraded`: complete successful bounded response lacks its static EXPECT marker.
  This is a heuristic, not proof of an outage, API correctness, or stale data.
- `blocked`: HTTP 403; **not** proof of Cloudflare or geographic blocking.
- `http_error`: other valid HTTP responses (including 401, 429 and 5xx).
- `dns_error`: curl could not resolve the endpoint hostname (exit 6); not proof
  a domain is dead. Proxy DNS errors are separate `proxy_error` (exit 5).
- `timeout`, `tls_error`, `network_error`, `redirect_error`: distinct curl failure
  classes. Transport failures take precedence over any partial HTTP response.
- `probe_error`: missing/broken probe tooling or malformed output. Such a run
  fails without publishing a new snapshot.
- `mixed`: differing observations; reserved for future multiple sources, never
  interpreted as evidence of geographic blocking.

Dashboard history retains old `dns_dead` and `geo_blocked_*` values with explicitly
legacy labels. Historical diagnoses are not recomputed. New schema version 2 uses
`observations.local`, and top-level `sources.local` describes that probe.

## Publication and failure handling

`check.py` alone builds date JSON, `latest.json`, `index.json`, and `history.json`.
It validates all historical day files under the writer lock **before endpoint
requests**, then revalidates before writing; corrupt data fails closed (including
an existing same-day file). Historical snapshots may omit `date` only when their
valid timezone-bearing ISO `checked_at` timestamp's YYYY-MM-DD matches the filename.
An explicit wrong/null date, invalid or mismatched timestamp, empty/missing portal
map, or malformed JSON is rejected. Legacy objects enter consolidated history
unchanged: no dates are added and no historical statuses/metadata are rewritten.
Each output is staged in the same directory, flushed and atomically replaced.
**Self-contained `history.json` is replaced last and is the dashboard's single
consistent publication unit.** Readers never assemble index/latest/day files.

Separate compatibility files are individually atomic, not a multi-file
transaction: interruption mid-replacement can leave them on different runs while
the dashboard still sees a complete old history. Rerun to repair; do not deploy
after a failed check. The directory is fsynced after publication; a filesystem
failure at that point may return failure even if the new history is visible.
History includes all retained date files, and repeated same-day checks replace
that day's observation (not an intraday log). UTC determines snapshot dates.

## Optional deployment

`bash status/check-and-deploy.sh [checker options]` is **check-only** by default.
No implicit git commit/push or credential-store lookup is performed. To deploy:

```sh
# Supply a token securely in the environment; never commit it.
export STATUS_PAGES_PROJECT='your-pages-project'
bash status/check-and-deploy.sh --deploy --workers 4
```

Requires a reviewed installed `wrangler` executable and `CLOUDFLARE_API_TOKEN`.
`STATUS_PAGES_BRANCH` defaults to `main`. `--output-dir` is forbidden in deployment
mode, preventing accidental publication of scratch results. A successful CLI
upload alone is not verification of the public deployment: confirm the exact
published history/site separately. Deployment was not exercised by offline tests.

## Regression tests

```sh
python3 -m unittest discover -s tests -p 'test_status*.py'
python3 scripts/test_status_canonical.py
# Optional: installed Playwright and compatible Chromium are required.
node scripts/test_status_layout.cjs
```

Tests use temporary directories, mocked curl results and a real curl loopback HTTP
fixture, plus an offline browser fixture when available; no monitored services or
tracked `status/data` are changed.
The layout test preserves dataset-derived counts, the canonical URL and 90-bar
geometry at mobile/tablet/desktop widths.
