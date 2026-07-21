```{include} ../README.md
:relative-docs: docs/
:relative-images:
```

# Welcome to my-g4public-orm Documentation

This is the SQLAlchemy ORM for the MySQL `g4public` database.

## Table of Contents

```{toctree}
:maxdepth: 2
:caption: Getting Started:

installation
quick-start
```

```{toctree}
:maxdepth: 2
:caption: API Reference:

api/index
```

```{toctree}
:maxdepth: 2
:caption: Architecture Decisions:

adr/index
```

## Overview

The `my-g4public-orm` package provides a typed, synchronous SQLAlchemy 2.0 ORM that maps to the existing MySQL schema of the HGNC public gene/family data (`pub_hgnc`, gene families, hierarchy, HCOP orthologs, GenCC, MANE, etc.).

The ORM gives full row-level CRUD (create / read / update / delete data) capabilities while maintaining compatibility with the existing database schema.

## Key Features

- Full SQLAlchemy 2.0 ORM implementation
- Maps to all 17 tables in the MySQL `g4public` database
- Synchronous only (no async engine/session)
- Read and write data only - never creates, alters, or drops schema objects
- Built on the shared `db-common` library
- Full unit test coverage with integration tests against a real MySQL database

## Modules

The package is organized into the following modules:

- `core`: Core models including `pub_hgnc`, `cell`, `family_new`, `family_alias`, `hierarchy`, `hierarchy_closure`, `locus_stats_chr`, `comment`, `gencc`, `mane`, `rat_mus_symbol`, `hcop_orthologs`
- `reference`: Reference data models including `external_resource`, `specialist`
- `association`: Junction models including `gene_has_family`, `family_has_external_resource`, `family_has_specialist`
- `repositories`: Generic CRUD repository base class
- `core.settings/session`: Core functionality including settings and session management
