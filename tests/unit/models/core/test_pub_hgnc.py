"""Test module for the pub_hgnc model."""

from my_g4public_orm.models.core.pub_hgnc import PubHgnc


def test_pub_hgnc_model_structure():
    """Test that the PubHgnc model has the correct structure."""
    # Check table name
    assert PubHgnc.__tablename__ == "pub_hgnc"

    # Check table has correct number of columns (58 total including PK)
    table = PubHgnc.__table__
    assert len(table.columns) == 58

    # Check column definitions match the dump
    # gd_hgnc_id is the primary key (forced ORM PK)
    assert "gd_hgnc_id" in table.columns
    assert table.c.gd_hgnc_id.primary_key is True
    assert table.c.gd_hgnc_id.type.__class__.__name__ == "Integer"

    # gd_app_sym should be String(50)
    assert "gd_app_sym" in table.columns
    assert table.c.gd_app_sym.type.__class__.__name__ == "String"
    assert table.c.gd_app_sym.type.length == 50

    # gd_status should be String(20) per the dump
    assert "gd_status" in table.columns
    assert table.c.gd_status.type.__class__.__name__ == "String"
    assert table.c.gd_status.type.length == 20

    # Date columns should have Date type
    date_columns = [
        "gd_date2app_or_res",
        "gd_date_mod",
        "gd_date_name_change",
        "gd_date_sym_change",
    ]
    for col_name in date_columns:
        assert col_name in table.columns
        assert table.c[col_name].type.__class__.__name__ == "Date"

    # gd_coord should exist (not md_coord)
    assert "gd_coord" in table.columns
    assert "md_coord" not in table.columns

    # Boolean columns (tinyint(1) in MySQL)
    bool_columns = ["gd_ambiguous", "gd_to_review", "gd_stable_symbol"]
    for col_name in bool_columns:
        assert col_name in table.columns
        assert table.c[col_name].type.__class__.__name__ == "Boolean"

    # Text columns
    text_columns = ["gd_aliases", "md_prot_id", "gd_coord"]
    for col_name in text_columns:
        assert col_name in table.columns
        assert table.c[col_name].type.__class__.__name__ == "Text"

    # Integer columns
    int_columns = ["md_eg_id", "md_agr"]
    for col_name in int_columns:
        assert col_name in table.columns
        assert table.c[col_name].type.__class__.__name__ == "Integer"


def test_pub_hgnc_indexes():
    """Test that the pub_hgnc model has the correct indexes."""
    # Should have 7 indexes, not including md_agr_index
    table = PubHgnc.__table__
    indexes = table.indexes
    index_names = {idx.name for idx in indexes}

    expected_indexes = {
        "pub_hgnc_gd_app_sym_index",
        "pub_hgnc_gd_hgnc_id_index",
        "pub_hgnc_gd_pub_eg_id_index",
        "pub_hgnc_gd_pub_ensembl_id_index",
        "pub_hgnc_md_eg_id_index",
        "pub_hgnc_md_ensembl_id_index",
        "pub_hgnc_md_vega_id_index",
    }

    assert index_names == expected_indexes
