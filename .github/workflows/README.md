# GitHub Actions Workflows

This directory holds the CI/CD gate for `my-g4public-orm`. It is adapted from
the `pg-g4public-orm` sibling with the MySQL substitutions noted below.

## Trigger policy

All day-to-day development happens on a `dev` branch and lands via a pull
request against `main`. No workflow triggers on `dev`, `develop`, or
`feature/*` branches — they fire only on `main`:

| Workflow          | `push: [main]` | `pull_request: [main]` |
| ----------------- | :------------: | :--------------------: |
| `ci.yml`          |       ✓        |           ✓            |
| `coverage.yml`    |       ✓        |           ✓            |
| `docs.yml`        |       ✓        |           ✓            |
| `security.yml`    |       ✓        |           ✓            |
| `development.yml` |       —        |           ✓            |

`release.yml` and `pages.yml` (added in a follow-up task) fire on
`push: [main]` only.

## `ci.yml`

A single matrixed job with two legs:

- **`unit`** — runs `pytest tests/unit` (no database required).
- **`integration`** — runs `pytest tests/integration` against a `mysql:8.0`
  service container (this is the MySQL edition). The integration tests spin up
  their own hermetic `testcontainers` `mysql:8.0` instance with
  `--character-set-server=utf8mb4 --collation-server=utf8mb4_bin`.

There is **no** `performance` leg.

## `security.yml`

Two security-focused jobs run on push/PR to `main`:

- **`dependency_audit`** — installs project dependencies and runs
  `pip-audit --local`.
- **`secret_scan`** — runs `gitleaks` against the repository history.

## MySQL substitutions vs the PostgreSQL sibling

- Service image: `mysql:8.0` (was `postgres:16` / testcontainers-only).
- Install extra: `.[test,mysql]` (was `.[test,postgres]`).
- Coverage target package: `src/my_g4public_orm` (was `src/pg_g4public_orm`).
