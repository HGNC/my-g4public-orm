# my-g4public-orm

SQLAlchemy 2.0 ORM for the MySQL `g4public` database (HGNC public gene/family data).

Built on the shared `db-common` library, mirroring the structure of `pg-g4public-orm`
but targeting **MySQL >= 8.0** (mysqlclient driver).

## Quick Start

Install with uv:

```bash
uv add my-g4public-orm
```

Or with pip:

```bash
pip install my-g4public-orm
```

Configure your database connection with environment variables:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=your_user
export DB_PASSWORD=your_password
export DB_NAME=g4public
```

Use in your application:

```python
from my_g4public_orm import (
    DatabaseSettings,
    FamilyNew,
    PubHgnc,
    Repository,
    get_readwrite_session,
    initialize_engine,
)

# Initialize the database engine
initialize_engine(DatabaseSettings())

# Use a session for database operations
with get_readwrite_session() as session:
    # Use the generic repository for CRUD operations
    gene_repo = Repository(session, PubHgnc)

    # Get a gene by HGNC ID
    gene = gene_repo.get_by_id(1234)

    # Create a new family
    family_repo = Repository(session, FamilyNew)
    new_family = FamilyNew(
        abbreviation="TEST",
        name="Test Family",
        type="G",
        desc_comment="A test gene family",
    )
    family_repo.add(new_family)
    session.commit()
```

## Models

The package provides ORM models for all 17 tables in the g4public schema:

### Core Tables
- `PubHgnc` - Main gene table with ~58 columns
- `Cell` - Cell type information
- `FamilyNew` - Gene family definitions
- `FamilyAlias` - Family name aliases
- `Hierarchy` - Family hierarchy relationships
- `HierarchyClosure` - Family hierarchy closure table
- `LocusStatsChr` - Locus statistics by chromosome
- `Comment` - Gene comments
- `Gencc` - GenCC gene-disease associations
- `Mane` - MANE gene transcripts
- `RatMusSymbol` - Rat/Mouse symbol mappings
- `HcopOrthologs` - HCOP orthologs with MySQL enum support

### Reference Tables
- `ExternalResource` - External resource definitions
- `Specialist` - Specialist curator information

### Association Tables
- `GeneHasFamily` - Gene-to-family relationships
- `FamilyHasExternalResource` - Family-to-resource relationships
- `FamilyHasSpecialist` - Family-to-specialist relationships

## Development

Install for development:

```bash
uv sync --all-extras
```

Run tests:

```bash
# Run unit tests
uv run pytest

# Run integration tests (requires Docker)
uv run pytest -m integration
```

Lint and type check:

```bash
uv run black --check src/ tests/
uv run ruff check .
uv run mypy src/my_g4public_orm
```

## Requirements

- Python >= 3.13
- MySQL >= 8.0
- `mysqlclient` >= 1.4 (for MySQL connectivity)

> **Status:** Alpha — under active development.
