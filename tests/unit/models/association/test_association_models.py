"""Test module for association (junction) models."""

from my_g4public_orm.models.association import (
    FamilyHasExternalResource,
    FamilyHasSpecialist,
    GeneHasFamily,
)


def _assert_primary_key_columns(table, expected_columns: list[str]) -> None:
    for column_name in expected_columns:
        assert column_name in table.columns
        assert table.c[column_name].primary_key is True


def _assert_column_types(table, expected_column_types: dict[str, str]) -> None:
    for column_name, type_name in expected_column_types.items():
        assert column_name in table.columns
        assert table.c[column_name].type.__class__.__name__ == type_name


def _assert_index_names(table, expected_indexes: set[str]) -> None:
    assert {index.name for index in table.indexes} == expected_indexes


def test_gene_has_family_model_structure():
    """gene_has_family has a composite PK and expected columns/indexes."""
    assert GeneHasFamily.__tablename__ == "gene_has_family"

    table = GeneHasFamily.__table__
    assert set(table.columns.keys()) == {"hgnc_id", "family_id", "url", "custom_sort"}

    _assert_primary_key_columns(table, ["hgnc_id", "family_id"])

    _assert_column_types(
        table,
        {
            "hgnc_id": "Integer",
            "family_id": "Integer",
            "url": "String",
            "custom_sort": "String",
        },
    )
    assert table.c.url.type.length == 255
    assert table.c.custom_sort.type.length == 255
    _assert_index_names(
        table,
        {"gene_has_family_family_id_index", "gene_has_family_hgnc_id_index"},
    )


def test_family_has_external_resource_model_structure():
    """family_has_external_resource has a composite PK and expected columns."""
    assert FamilyHasExternalResource.__tablename__ == "family_has_external_resource"

    table = FamilyHasExternalResource.__table__
    assert set(table.columns.keys()) == {"family_id", "ext_id"}

    _assert_primary_key_columns(table, ["family_id", "ext_id"])
    _assert_column_types(table, {"family_id": "Integer", "ext_id": "Integer"})


def test_family_has_specialist_model_structure():
    """family_has_specialist has a composite PK and expected columns/indexes."""
    assert FamilyHasSpecialist.__tablename__ == "family_has_specialist"

    table = FamilyHasSpecialist.__table__
    assert set(table.columns.keys()) == {"fam_id", "specialist_id"}

    _assert_primary_key_columns(table, ["fam_id", "specialist_id"])
    _assert_column_types(table, {"fam_id": "Integer", "specialist_id": "Integer"})
    _assert_index_names(
        table,
        {
            "family_has_specialist_fam_id_index",
            "family_has_specialist_specialist_id_index",
        },
    )
