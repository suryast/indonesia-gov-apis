# Contributing

## Local setup and offline checks

Python 3.11–3.14 are tested in CI; `.python-version` selects 3.14, a supported
GitHub-hosted Linux runtime verified on 2026-10-10. curl is required for the
monitor, not for mocked example tests. The site has no framework/build pipeline.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip check
python scripts/check_repository.py
python -m pip_audit -r requirements.txt --no-deps --disable-pip
python -m pip_audit -r requirements-dev.txt --no-deps --disable-pip
```

The check runner executes `unittest discover -s tests -p 'test_*.py'`, the existing
canonical test, `python scripts/validate_catalog.py`, scoped Ruff checks, and
offline zizmor workflow security analysis.
No offline gate probes services or changes `status/data`. Synthetic fixtures are
not published as government data. CI also runs the original browser layout gate.
For a focused example test: `python -m unittest discover -s tests -p test_examples.py`.

### Optional browser test (Node 24)

Playwright is isolated under `.github/browser-tests/` with an exact version and
npm integrity lockfile, not an application framework or site build dependency:

```sh
npm ci --prefix .github/browser-tests --ignore-scripts
.github/browser-tests/node_modules/.bin/playwright install chromium
PLAYWRIGHT_MODULE="$PWD/.github/browser-tests/node_modules/playwright" node scripts/test_status_layout.cjs
npm audit --prefix .github/browser-tests
```

Linux CI additionally installs Chromium's system dependencies using Playwright's
`install --with-deps chromium`. Existing `CHROMIUM_PATH`, `STATUS_HTML` and
`STATUS_LAYOUT_OUTPUT` overrides are supported by the unchanged test.

## Examples and opt-in live checks

Every example supports `--help`. BI/BPS return nonzero on network, HTTP or schema
failure. They do not retry or evade access controls. Portal guidance commands
make **no requests**, and cannot confirm certification or financial legitimacy.

```sh
python examples/bi_exchange.py --timeout 10
# Set BPS_API_KEY securely in your environment; do not pass keys on the CLI.
# Discover the correct variable/domain in the official BPS developer portal.
python examples/bps_inflation.py --variable YOUR_NUMERIC_VARIABLE --domain 0000 --timeout 10
python examples/search_halal.py 'Product or business name'
python examples/check_ojk.py 'Exact legal entity name'
```

`YOUR_NUMERIC_VARIABLE` is a placeholder, not an indicator ID. The historical
`bps_inflation.py` filename does not imply that variable 1 or any arbitrary ID
means CPI/inflation. Output retains BPS dimension metadata and `datacontent`
instead of guessing year/value rows. BI preserves currency units, sell/buy labels
and locale strings; it is the **transaction-rate** page, not a JISDOR API.

For live verification, record date/time, official URL, authentication requirement,
HTTP result and actual response shape without keys, response PII or raw keyed
URLs. Compare BI against the same official page and verify BPS dimensions before
interpreting values. An inaccessible page is not evidence of missing data.
Halal supervisor directories do not prove product certification. For OJK, check
FIND and official warnings, exact legal identity and relevant licence/activity;
absence from a warning list never proves licensed, legal or safe.

Monitor live checks are a separate opt-in operation. Write outside tracked data:

```sh
python status/check.py --output-dir /path/to/new-monitor-trial --timeout 10 --workers 4
```

Describe only a verified probe location/provider via the monitor's source options;
otherwise leave its metadata unconfigured. See `status/README.md` for semantics.
Do not run the deployment wrapper merely to validate code.

## Catalog edits

Use official sources, distinguish documented APIs from portal-only access,
registration, integrations and scraping. Do not copy unverified code snippets as
working examples. Run `python scripts/validate_catalog.py` after documentation
changes; it validates local consistency, not live reachability.

## Dependency and CI updates

Runtime pins and their transitive dependencies are in `requirements.txt`;
`requirements-dev.txt` pins the complete developer environment. `pyproject.toml`
records the two direct runtime pins and Ruff scope; it is not a site framework.
Use a fresh virtual environment to resolve updates, check current PyPI releases
and `Requires-Python`, update both locks and direct metadata consistently, then
run installs, `pip check`, audits and regression tests. Do not freeze unrelated
packages from a shared/global environment. All release pins here were verified
against PyPI on 2026-10-10. Exact pins are not cryptographic hash locks; audit
results are a time-bound advisory check, not a security guarantee.

Actions are full commit SHAs, verified by resolving the latest stable upstream
GitHub release/tag to its commit on 2026-10-10: checkout v7.0.1, setup-python
v7.0.0, setup-node v7.1.0, wrangler-action v4.1.3, upload-artifact v7.0.2 and
download-artifact v8.0.2. Verify the release and dereference
annotated tags before updating a pin. Wrangler 4.149.0 and Playwright 1.64.0 were
verified against npm; Node 24 satisfies Wrangler's Node >=22 requirement and the
Cloudflare action uses Node 24. Dependabot proposes pip/actions/browser-tooling
updates; review all pins and preserve security constraints. Wrangler's workflow
version literal must also be reviewed manually. Package-manager caches are
explicitly disabled in CI, including the privileged deploy job.

CI uses read-only permissions and no persisted checkout credentials. Scheduled
monitoring runs on main only, with bounded timeout/concurrency. Its job alone has
contents-write for allowlisted monitoring JSON commits; a concurrent main update
may reject its non-forced push, in which case retry rather than rebasing generated
data blindly. Branch protection can also prevent automated pushes; keep it intact.

Scheduled Cloudflare deployment preserves the existing daily behavior and uses
the existing scoped `CLOUDFLARE_API_TOKEN` secret, failing closed if it is absent
or invalid. No new Actions variable is required. The workflow targets the confirmed `gov-portal-status`
Pages project, production branch `main`, account `bb88d649c15e3a7bd66000a5467ca3ad`.
The account identifier is not a credential; no additional secret is required.
The separate read-only deploy job uses the `production` GitHub environment.
Review its allowed branches/reviewer protections without unintentionally pausing the daily schedule;
a named environment alone does not enforce approvals. The monitor job receives
no Cloudflare secret. Deploy consumes only its same-run static artifact, retained
for three days, without checking out or running status source scripts.
Publish only the new staging directory built by `--stage-static`, never `status/`
itself. The stager allowlists HTML/image/font assets and validated JSON, refuses
symlinks, excludes scripts and arbitrary files, and refuses existing destinations.
Confirm the public site/data after any actual deployment; local tests do not
exercise GitHub permissions or Cloudflare credentials/account configuration.
The local `status/check-and-deploy.sh --deploy` wrapper also stages only this
allowlist into a fresh temporary directory and removes it on success or failure;
its default remains check-only. Offline deploy tests mock network-bearing checker
and Wrangler commands but execute the real stager, assert script exclusion and
verify cleanup before deleting their fixtures.
