"""Test module for family group models."""

from my_g4public_orm.models.core import (
    FamilyAlias,
    FamilyNew,
    Hierarchy,
    HierarchyClosure,
)


def test_family_new_model_structure():
    """Test that the FamilyNew model has the correct structure."""
    # Check table name
    assert FamilyNew.__tablename__ == "family_new"

    # Check table has correct columns
    table = FamilyNew.__table__

    # Check id is primary key
    assert "id" in table.columns
    assert table.c.id.primary_key is True
    assert table.c.id.type.__class__.__name__ == "Integer"

    # Check other columns exist with correct types
    expected_columns = {
        "abbreviation": "String",
        "name": "String",
        "editor": "String",
        "curator_comment": "Text",
        "status": "String",
        "external_note": "Text",
        "pubmed_ids": "Text",
        "type": "String",
        "desc_comment": "Text",
        "desc_label": "String",
        "desc_source": "String",
        "desc_go": "String",
        "typical_gene": "String",
    }

    for col_name, type_name in expected_columns.items():
        assert col_name in table.columns
        assert table.c[col_name].type.__class__.__name__ == type_name

    # Check indexes
    indexes = table.indexes
    index_names = {idx.name for idx in indexes}

    expected_indexes = {
        "family_new_abbreviation_index",
        "family_new_name_index",
    }

    assert expected_indexes.issubset(index_names)


def test_family_alias_model_structure():
    """Test that the FamilyAlias model has the correct structure."""
    # Check table name
    assert FamilyAlias.__tablename__ == "family_alias"

    # Check table has correct columns
    table = FamilyAlias.__table__

    # Check id is primary key (forced ORM PK)
    assert "id" in table.columns
    assert table.c.id.primary_key is True
    assert table.c.id.type.__class__.__name__ == "Integer"

    # Check other columns exist
    assert "family_id" in table.columns
    assert "alias" in table.columns


def test_hierarchy_model_structure():
    """Test that the Hierarchy model has the correct structure."""
    # Check table name
    assert Hierarchy.__tablename__ == "hierarchy"

    # Check table has correct columns with composite primary key
    table = Hierarchy.__table__

    # Check composite primary key
    assert "parent_fam_id" in table.columns
    assert "child_fam_id" in table.columns

    # Check that both columns make up the primary key
    primary_key_columns = [col.name for col in table.primary_key.columns]
    assert "parent_fam_id" in primary_key_columns
    assert "child_fam_id" in primary_key_columns

    # Check indexes
    indexes = table.indexes
    index_names = {idx.name for idx in indexes}

    expected_indexes = {
        "hierarchy_child_fam_id_index",
        "hierarchy_parent_fam_id_index",
    }

    assert expected_indexes.issubset(index_names)


def test_hierarchy_closure_model_structure():
    """Test that the HierarchyClosure model has the correct structure."""
    # Check table name
    assert HierarchyClosure.__tablename__ == "hierarchy_closure"

    # Check table has correct columns with composite primary key (2 cols only)
    table = HierarchyClosure.__table__

    # Check composite primary key (parent_fam_id, child_fam_id) - 2 cols only
    assert "parent_fam_id" in table.columns
    assert "child_fam_id" in table.columns
    assert "distance" in table.columns

    # Check that ONLY parent_fam_id and child_fam_id make up the primary key
    # distance should be a plain nullable column, NOT part of the PK
    primary_key_columns = [col.name for col in table.primary_key.columns]
    assert "parent_fam_id" in primary_key_columns
    assert "child_fam_id" in primary_key_columns
    assert "distance" not in primary_key_columns

    # distance should be a plain nullable Integer column
    assert table.c.distance.type.__class__.__name__ == "Integer"
    assert table.c.distance.nullable is True

    # Check indexes
    indexes = table.indexes
    index_names = {idx.name for idx in indexes}

    expected_indexes = {
        "hierarchy_closure_child_fam_id_index",
        "hierarchy_closure_parent_fam_id_index",
    }

    assert expected_indexes.issubset(index_names)
