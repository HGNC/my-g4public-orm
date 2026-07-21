# ADR 0001: Version Source of Truth for Package and Docs

- **Status:** Accepted
- **Date:** 2026-07-21

## Context

The package version lives in `pyproject.toml` and drives release automation.
Historically, `docs/conf.py` also carried a hardcoded Sphinx `release` value.
This creates drift risk during release bumps.

The repository also declared Python 3.14 support via Trove classifier while
project tooling/CI targets Python 3.13, which can overstate verified support.

## Decision

1. `pyproject.toml` is the single source of truth for versioning.
2. Sphinx `release` must be derived from `pyproject.toml` at build time.
3. Python version classifiers should only claim versions verified by current
   tooling/CI.

## Consequences

### Positive

- Docs and package metadata stay aligned automatically.
- Release automation is less error-prone.
- Published support claims better match tested reality.

### Trade-offs

- `docs/conf.py` now reads and parses `pyproject.toml` at build time.
- Future Python version classifier upgrades require corresponding CI/tooling updates.

## Validation

The following checks enforce this decision:

- `tests/unit/test_docs_consistency.py::test_docs_conf_release_matches_pyproject_version`
- `tests/unit/test_docs_consistency.py::test_python_classifiers_match_tested_versions`
