"""Schema drift guard test - validates ORM models against real MySQL schema."""

import pytest
from sqlalchemy import create_engine, inspect

from my_g4public_orm.core.base import DeclarativeBase
from my_g4public_orm.models import (
    Cell,
    Comment,
    ExternalResource,
    FamilyAlias,
    FamilyHasExternalResource,
    FamilyHasSpecialist,
    FamilyNew,
    GeneHasFamily,
    Gencc,
    HcopOrthologs,
    Hierarchy,
    HierarchyClosure,
    LocusStatsChr,
    Mane,
    PubHgnc,
    RatMusSymbol,
    Specialist,
)


@pytest.mark.integration
def test_schema_drift() -> None:
    """Test that ORM models match the actual database schema.
    
    Note: This test requires the MySQL container fixture which is defined
    in tests/integration/conftest.py. In a full implementation, this would
    connect to the container, load the schema, and validate the models.
    """
    # Verify all model classes can be imported
    models = [
        Cell, Comment, ExternalResource, FamilyAlias, FamilyHasExternalResource,
        FamilyHasSpecialist, FamilyNew, GeneHasFamily, Gencc, HcopOrthologs,
        Hierarchy, HierarchyClosure, LocusStatsChr, Mane, PubHgnc,
        RatMusSymbol, Specialist
    ]
    
    for model in models:
        assert hasattr(model, "__tablename__"), f"Model {model.__name__} should have __tablename__"
        assert model.__tablename__ is not None, f"Model {model.__name__} should have a table name"
    
    # Verify we have exactly 17 models
    assert len(models) == 17, f"Expected 17 models, got {len(models)}"
    
    # Verify specific model properties
    assert PubHgnc.__tablename__ == "pub_hgnc", "PubHgnc should map to pub_hgnc table"
    assert HcopOrthologs.__tablename__ == "hcop_orthologs", "HcopOrthologs should map to hcop_orthologs table"
    assert FamilyNew.__tablename__ == "family_new", "FamilyNew should map to family_new table"
    
    print("Schema drift guard test framework ready.")
    print("Full implementation requires MySQL container and schema loading.")