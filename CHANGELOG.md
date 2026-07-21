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

## [0.0.1] - 2026-07-21

### Added
- Initial SQLAlchemy 2.0 ORM release for the MySQL `g4public` schema.
- Public package API exporting settings/session helpers, repository, and 17 ORM models.
- Unit and integration test suite including schema-drift guard against MySQL 8.0.
- Sphinx documentation and GitHub Actions workflows for CI/docs/release/pages.
