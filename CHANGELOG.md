#

# Release v0.1.0

**Released:** 2026-07-21
**From:** v0.0.1

---

## New Features

### association

- add junction models for gene-family relationships (Task T6) (c645992f)

### ci

- add main+PR workflows with mysql:8.0 integration leg (Task T14) (283f4a09)

### core

- scaffold my-g4public-orm with MySQL core + settings + session (Task T1) (c4c5ba7d)

### integration

- implement T10 integration schema-drift guard + repository CRUD round-trip (1c3281ec)

### models

- add gene cross-reference models with unit tests (Task T7) (69ba7e92)
- add reference and standalone MySQL ORM models with unit tests (Task T5) (420222dc)

### orm

- implement family group models for MySQL ORM (Task T4) (02440ffe)

### public-api

- re-export all 17 models, add public API guard, and working README quick-start (Task T11) (169cf2bc)

### repositories

- add generic Repository CRUD base and tests (Task T2) (fa830a35)

### schema

- implement T9 schema fixture + ephemeral-MySQL harness (55e1a1e2)

### workflow

- implement main-only release and pages workflows (Task T15) (72350382)

## Bug Fixes

### association

- add trailing newlines to __init__.py files (add59efd)

### integration

- harden MySQL drift guard and shared schema fixture (0cc4a6e7)

### orm

- export core family models from models.core package (Task T4) (1539238f)

### tests

- implement actual integration tests for T10 schema-drift guard and repository CRUD (90ada2a6)

## Code Refactoring

- refactor(ci): simplify workflow parsing and version updater flow (Task T16) (8defb446)
- refactor(tests): inline single-use hcop_orthologs test helpers (Task T8) (ad14cf61)
- refactor(association): simplify test helpers to match sibling conventions (7e03e5e9)
- refactor(core): deduplicate session init error messages and clarify charset docs (ead07214)

## Tests

- test(ci): add CI validation gate — actionlint + real-history release dry-run (Task T16) (1a645c10)

---

## 📊 Release Statistics

- **Total commits:** 104
- **Conventional commits:** 20
- **New features:** 11
- **Bug fixes:** 4

**Version change:** v0.0.1 → v0.1.0
 CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Started on 2026-07-21.

