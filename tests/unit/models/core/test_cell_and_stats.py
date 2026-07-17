"""Test module for cell and locus_stats_chr models."""

from my_g4public_orm.models.core import Cell, LocusStatsChr


def _assert_column_types(table, expected_column_types: dict[str, str]) -> None:
    for column_name, type_name in expected_column_types.items():
        assert column_name in table.columns
        assert table.c[column_name].type.__class__.__name__ == type_name


def _assert_primary_key_columns(table, expected_columns: list[str]) -> None:
    for column_name in expected_columns:
        assert column_name in table.columns
        assert table.c[column_name].primary_key is True


def test_cell_model_structure():
    """Test that the Cell model has the correct structure."""
    assert Cell.__tablename__ == "cell"
    table = Cell.__table__

    _assert_primary_key_columns(table, ["cell_id"])
    assert table.c.cell_id.type.__class__.__name__ == "Integer"
    _assert_column_types(
        table,
        {
            "cell_name": "String",
            "cell_alias": "String",
            "cell_table": "String",
            "cell_permit": "Text",
            "cell_view": "Text",
            "cell_edit": "Text",
            "cell_lint": "Text",
            "cell_notes": "Text",
            "cell_sort": "Integer",
        },
    )


def test_locus_stats_chr_model_structure():
    """Test that the LocusStatsChr model has the correct structure."""
    assert LocusStatsChr.__tablename__ == "locus_stats_chr"
    table = LocusStatsChr.__table__

    _assert_primary_key_columns(table, ["ls_chr", "ls_type", "ls_group", "ls_source"])
    _assert_column_types(
        table,
        {
            "ls_chr": "String",
            "ls_type": "String",
            "ls_group": "String",
            "ls_source": "String",
            "ls_count": "Integer",
            "ls_sort": "Integer",
            "ls_date": "String",
        },
    )
    assert table.c.ls_date.type.length == 255
