# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Documentation consistency regression tests to guard metadata drift.
- `security.yml` GitHub Actions workflow with dependency (`pip-audit`) and secret (`gitleaks`) scanning on push/PR to `main`.

### Changed
- Sphinx `docs/conf.py` now reads `release` from `pyproject.toml`.
- Removed unverified Python 3.14 classifier from package metadata.

## [0.1.0] - 2026-07-21

### Added
- Junction association models for gene-family relationships.
- Main+PR GitHub Actions workflows with MySQL integration coverage.
- Core ORM scaffolding with MySQL settings/session management.
- Integration schema-drift guard and repository CRUD round-trip coverage.
- Gene cross-reference models and tests.
- Reference/standalone MySQL ORM models and tests.
- Family group ORM models.
- Public API exports for all 17 models plus package quick-start.
- Generic `Repository` CRUD base and tests.
- Schema fixture with ephemeral MySQL test harness.
- Release and Pages workflows.

### Fixed
- Trailing newlines for association package `__init__.py` modules.
- Hardened MySQL schema-drift guard and shared schema fixture.
- Core family model exports from `models.core`.
- Integration test coverage for schema-drift guard and CRUD behavior.

### Changed
- Simplified workflow parsing and version updater flow.
- Inlined single-use HCOP ortholog test helpers.
- Simplified association test helpers to match sibling conventions.
- Deduplicated session-init error messages and clarified charset docs.
- Added CI validation gate (actionlint + release dry-run over real history).

## [0.0.1] - 2026-07-21

### Added
- Initial SQLAlchemy 2.0 ORM release for the MySQL `g4public` schema.
- Public package API exporting settings/session helpers, repository, and 17 ORM models.
- Unit and integration test suite including schema-drift guard against MySQL 8.0.
- Sphinx documentation and GitHub Actions workflows for CI/docs/release/pages.
