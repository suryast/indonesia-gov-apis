# Repository guidance for agents

This repository contains a public-source catalog, executable Python examples, a
Python/curl status monitor and a deployable **static** HTML dashboard. It is not
an application framework project. Do not add npm/framework tooling solely for
the catalog or dashboard; the optional layout test uses isolated Playwright.

## Layout and boundaries

- `README.md`, `SKILL.md`, `apis/`, `references/`, `mcp-servers/`: catalog and documentation.
- `examples/`: command-line Python examples; requests + Beautiful Soup are the only
  runtime dependencies. OJK and halal examples intentionally print manual guidance
  and make no requests: unverified endpoints are not working public APIs.
- `status/check.py`: standard-library monitor using curl. See `status/README.md`.
  It writes monitoring JSON only when explicitly run. Never run it as an offline test.
- `status/index.html`, images/font and `status/data/*.json`: static site and retained
  observations. History is evidence, not a licence or certification database.
- `tests/`: offline unittest suites. `scripts/test_status_canonical.py` and
  `scripts/test_status_layout.cjs` are read-only regression gates; preserve them.
- `scripts/validate_catalog.py`: catalog/documentation consistency validator.
- `scripts/check_repository.py`: offline check runner and static-only deployment stager.
- `.github/`: pinned CI actions, Dependabot and bounded scheduled monitoring.

## Development

Use Python 3.11–3.14 (preferred version in `.python-version`). Install
`requirements-dev.txt` in a virtual environment. Run:

```sh
python scripts/check_repository.py
python -m pip check
python -m pip_audit -r requirements-dev.txt --no-deps --disable-pip
```

See `CONTRIBUTING.md` for browser tests, scoped live checks and dependency updates.
Tests mock public responses; passing offline tests do not verify live endpoints.

## Change discipline

Read git status and scoped files before editing. Preserve other workers' changes.
Do not rewrite generated monitoring data, run deploy scripts, commit or push
unless the task explicitly authorizes it. Edit source, then run the relevant tests.
Do not expose credentials/PII in examples, logs, commits or static output.
Use timeouts, `raise_for_status`, explicit authentication and guarded parsing.
Do not invent authless endpoints, stable variable meanings or unsupported result
schemas. Use official portal guidance when public API access is unverified.
No OJK alert-list match is not evidence of licensing, legality or safety; halal
supervisor records are not certification records.

Deployment must use `scripts/check_repository.py --stage-static NEW_DIRECTORY`:
only named HTML/image/font assets and allowlisted JSON are copied. Never publish
all of `status/`, Python/shell scripts, configuration or private keys.
