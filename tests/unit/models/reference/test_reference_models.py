"""Test module for reference models."""

from my_g4public_orm.models.reference import ExternalResource, Specialist


def _assert_integer_primary_key(table, column_name: str) -> None:
    assert column_name in table.columns
    column = table.c[column_name]
    assert column.primary_key is True
    assert column.type.__class__.__name__ == "Integer"


def _assert_column_types(table, expected_column_types: dict[str, str]) -> None:
    for column_name, type_name in expected_column_types.items():
        assert column_name in table.columns
        assert table.c[column_name].type.__class__.__name__ == type_name


def test_external_resource_model_structure():
    """Test that the ExternalResource model has the correct structure."""
    assert ExternalResource.__tablename__ == "external_resource"
    table = ExternalResource.__table__

    _assert_integer_primary_key(table, "id")
    _assert_column_types(
        table,
        {
            "name": "String",
            "url": "String",
            "description": "String",
            "approved": "Boolean",
        },
    )


def test_specialist_model_structure():
    """Test that the Specialist model has the correct structure."""
    assert Specialist.__tablename__ == "specialist"
    table = Specialist.__table__

    _assert_integer_primary_key(table, "id")
    _assert_column_types(
        table,
        {
            "name": "String",
            "url": "String",
            "address": "Text",
        },
    )
