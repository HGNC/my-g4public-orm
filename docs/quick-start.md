# Quick Start Guide

This guide will help you get started with `my-g4public-orm` quickly.

## Basic Usage

First, make sure you have configured your database connection using environment variables:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_NAME=g4public
```

### Initializing the Engine

```python
from my_g4public_orm.core.session import initialize_engine
from my_g4public_orm.core.settings import DatabaseSettings

# Initialize the database engine
settings = DatabaseSettings()
initialize_engine(settings)
```

### Querying Data

```python
from my_g4public_orm import PubHgnc
from my_g4public_orm.repositories import Repository
from my_g4public_orm.core.session import get_readwrite_session

# Create a repository for the PubHgnc model
with get_readwrite_session() as session:
    repo = Repository(session, PubHgnc)

    # Get a gene by HGNC ID
    gene = repo.get_by_id(12345)

    # List all genes
    genes = repo.list_all()

    # Filter genes by symbol
    genes = repo.filter_by(gd_app_sym="BRCA1")
```

### Creating New Records

```python
from my_g4public_orm import FamilyNew
from my_g4public_orm.core.session import get_readwrite_session

# Create a new family
family = FamilyNew(
    abbreviation="TEST",
    name="Test Family",
    status="Active",
    type="Test",
    desc_comment="A test family for demonstration"
)

# Add to database
with get_readwrite_session() as session:
    session.add(family)
    session.commit()
```

### Updating Records

```python
from my_g4public_orm.core.session import get_readwrite_session
from my_g4public_orm.models.core.family_new import FamilyNew

# Get a family by ID and update it
with get_readwrite_session() as session:
    # Get a family by ID
    family = session.get(FamilyNew, 1)

    # Update the family
    family.desc_comment = "Updated description"
    session.commit()
```

### Deleting Records

```python
from my_g4public_orm.core.session import get_readwrite_session
from my_g4public_orm.models.core.family_new import FamilyNew

# Get a family by ID and delete it
with get_readwrite_session() as session:
    # Get a family by ID
    family = session.get(FamilyNew, 1)

    # Delete the family
    session.delete(family)
    session.commit()
```

## Working with Related Data

The ORM provides access to all 17 tables in the g4public database:

```python
from my_g4public_orm import PubHgnc
from my_g4public_orm.repositories import Repository
from my_g4public_orm.core.session import get_readwrite_session

# Get a gene and its associated families
with get_readwrite_session() as session:
    repo = Repository(session, PubHgnc)
    gene = repo.get_by_id(12345)
    # Note: Direct relationship navigation is not implemented
    # You need to query associated tables manually
```

## Read-only Sessions

For read-only operations, use a read-only session:

```python
from my_g4public_orm.core.session import get_readonly_session, ReadOnlySessionError

# Get a read-only session
with get_readonly_session() as ro_session:
    # This will raise ReadOnlySessionError on commit
    try:
        ro_session.commit()
    except ReadOnlySessionError:
        print("Cannot commit on read-only session")
```

## Error Handling

The ORM raises standard SQLAlchemy exceptions:

```python
from sqlalchemy.exc import IntegrityError
from my_g4public_orm.core.session import get_readwrite_session
from my_g4public_orm.models.core.family_new import FamilyNew

try:
    # Attempt to insert duplicate data
    with get_readwrite_session() as session:
        family = FamilyNew(
            abbreviation="TEST",
            name="Test Family",
            status="Active",
            type="Test",
            desc_comment="A test family for demonstration"
        )
        session.add(family)
        session.commit()
except IntegrityError as e:
    print(f"Database integrity error: {e}")
```

## Closing Sessions

Always close sessions when done:

```python
from my_g4public_orm.core.session import close_all_sessions

# Close all sessions
close_all_sessions()
```

This concludes the quick start guide. For more detailed information, see the API Reference section.
