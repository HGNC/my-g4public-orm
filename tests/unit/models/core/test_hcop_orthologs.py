"""Tests for the ``hcop_orthologs`` model.

HCOP (HCOP Comparison of Orthology Predictions) pairwise ortholog rows.

Driven by the authoritative dump ``.ai/specs/my-g4public.sql`` (the real
Navicat DDL of ``g4public``). These are unit tests asserting SQLAlchemy
metadata (table name, full column set, types, nullability, the real ORM
primary key on ``orth_id``, the ``class_a``/``class_b`` MySQL ``ENUM`` types,
and the MySQL-specific kwargs) — no database required.
"""

from __future__ import annotations

import pytest
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Integer, String, Text, inspect


# ---------------------------------------------------------------------------
# Helpers (mirrors tests/unit/models/core/test_gene_xref_models.py)
# ---------------------------------------------------------------------------
def _column(model, column_name: str):
    """Return a mapped column by name."""
    return inspect(model).columns[column_name]


def _assert_column_type_and_nullability(
    model, column_name: str, expected_columns: dict[str, tuple[type, bool]]
) -> None:
    """Assert mapped column type and nullability against expected metadata."""
    col = _column(model, column_name)
    expected_type, expected_nullable = expected_columns[column_name]
    assert isinstance(col.type, expected_type), (
        f"{column_name}: expected {expected_type.__name__}, "
        f"got {type(col.type).__name__}"
    )
    assert (
        col.nullable is expected_nullable
    ), f"{column_name}: nullable={col.nullable}, expected {expected_nullable}"


# ===========================================================================
# HcopOrthologs
# ===========================================================================
@pytest.fixture(scope="module")
def hcop_orthologs():
    """Import the model lazily so collection succeeds before it exists."""
    from my_g4public_orm.models.core.hcop_orthologs import HcopOrthologs

    return HcopOrthologs


# All 31 ``hcop_orthologs`` columns transcribed verbatim from my-g4public.sql.
# The authoritative MySQL dump declares 31 columns for this table.
EXPECTED_HCOPY_COLUMNS: dict[str, tuple[type, bool]] = {
    # --- Identifiers ---
    "orth_id": (Integer, False),  # real PK (AUTO_INCREMENT)
    # --- Taxonomy ---
    "taxon_a": (Integer, False),  # NOT NULL
    "taxon_b": (Integer, False),  # NOT NULL
    # --- Cross-database identifiers ---
    "db_id_a": (String, False),  # NOT NULL
    "db_id_b": (String, False),  # NOT NULL
    "vgnc_a": (String, True),  # nullable
    "vgnc_b": (String, True),  # nullable
    "ensembl_a": (String, False),  # NOT NULL
    "ensembl_b": (String, False),  # NOT NULL
    "entrez_a": (String, True),  # nullable
    "entrez_b": (String, True),  # nullable
    # --- Symbol + gene names ---
    "symbol_a": (String, True),  # nullable
    "symbol_b": (String, True),  # nullable
    "symbol_source_a": (String, True),  # nullable
    "symbol_source_b": (String, True),  # nullable
    "name_a": (Text, True),  # mediumtext -> Text, nullable
    "name_b": (Text, True),  # mediumtext -> Text, nullable
    # --- Source / locus metadata ---
    "source_name_a": (String, True),  # nullable
    "source_name_b": (String, True),  # nullable
    "locus_type_a": (String, True),  # nullable
    "locus_type_b": (String, True),  # nullable
    "locus_source_a": (String, True),  # nullable
    "locus_source_b": (String, True),  # nullable
    # --- class_a / class_b: MySQL ENUM (not varchar) ---
    "class_a": (SAEnum, True),  # enum('Gene','Approved'), nullable
    "class_b": (SAEnum, True),  # enum('Gene','Approved'), nullable
    # --- Chromosomes / support / links ---
    "chr_a": (String, True),  # nullable
    "chr_b": (String, True),  # nullable
    "support": (String, False),  # NOT NULL
    "text_link_a": (Text, False),  # mediumtext -> Text, NOT NULL
    "text_link_b": (Text, False),  # mediumtext -> Text, NOT NULL
    "sort_order": (Integer, False),  # NOT NULL
}

HCOPY_VARCHAR_LENGTHS: dict[str, int] = {
    "db_id_a": 10,
    "db_id_b": 25,
    "vgnc_a": 28,
    "vgnc_b": 28,
    "ensembl_a": 28,
    "ensembl_b": 28,
    "entrez_a": 28,
    "entrez_b": 28,
    "symbol_a": 25,
    "symbol_b": 40,
    "symbol_source_a": 128,
    "symbol_source_b": 128,
    "source_name_a": 128,
    "source_name_b": 128,
    "locus_type_a": 255,
    "locus_type_b": 255,
    "locus_source_a": 128,
    "locus_source_b": 128,
    "chr_a": 128,
    "chr_b": 128,
    "support": 255,
}

HCOPY_TEXT_COLUMNS = {"name_a", "name_b", "text_link_a", "text_link_b"}

HCOPY_NOT_NULL_COLUMNS = {
    "orth_id",
    "taxon_a",
    "taxon_b",
    "db_id_a",
    "db_id_b",
    "ensembl_a",
    "ensembl_b",
    "support",
    "text_link_a",
    "text_link_b",
    "sort_order",
}

HCOPY_ENUM_VALUES = {"Gene", "Approved"}


def test_hcop_orthologs_tablename(hcop_orthologs) -> None:
    """``__tablename__`` must be the exact ``hcop_orthologs``."""
    assert hcop_orthologs.__tablename__ == "hcop_orthologs"


def test_hcop_orthologs_full_column_set(hcop_orthologs) -> None:
    """Every dump column is present and no extra columns are declared."""
    assert set(inspect(hcop_orthologs).columns.keys()) == set(EXPECTED_HCOPY_COLUMNS)


def test_hcop_orthologs_column_count_matches_dump(hcop_orthologs) -> None:
    """The dump declares exactly 31 columns for ``hcop_orthologs``."""
    assert len(inspect(hcop_orthologs).columns) == 31


@pytest.mark.parametrize("column_name", sorted(EXPECTED_HCOPY_COLUMNS))
def test_hcop_orthologs_column_types_and_nullability(
    hcop_orthologs, column_name: str
) -> None:
    """Each column has the right type and nullability per the dump."""
    _assert_column_type_and_nullability(
        hcop_orthologs, column_name, EXPECTED_HCOPY_COLUMNS
    )


@pytest.mark.parametrize("column_name", sorted(HCOPY_TEXT_COLUMNS))
def test_hcop_orthologs_text_columns(hcop_orthologs, column_name: str) -> None:
    """``name_a``/``name_b``/``text_link_*`` are ``mediumtext`` -> Text."""
    assert isinstance(_column(hcop_orthologs, column_name).type, Text)


@pytest.mark.parametrize("column_name", sorted(HCOPY_NOT_NULL_COLUMNS))
def test_hcop_orthologs_not_null_columns(hcop_orthologs, column_name: str) -> None:
    """The NOT NULL columns are non-nullable per the dump."""
    assert _column(hcop_orthologs, column_name).nullable is False


@pytest.mark.parametrize("column_name", sorted(HCOPY_VARCHAR_LENGTHS))
def test_hcop_orthologs_varchar_lengths(hcop_orthologs, column_name: str) -> None:
    """``varchar(N)`` columns carry the dump's length."""
    col = _column(hcop_orthologs, column_name)
    assert isinstance(col.type, String), column_name
    assert col.type.length == HCOPY_VARCHAR_LENGTHS[column_name], (
        f"{column_name}: length={col.type.length}, "
        f"expected {HCOPY_VARCHAR_LENGTHS[column_name]}"
    )


def test_hcop_orthologs_orth_id_is_real_primary_key(hcop_orthologs) -> None:
    """``orth_id`` is the real primary key (AUTO_INCREMENT)."""
    assert [c.name for c in inspect(hcop_orthologs).primary_key] == ["orth_id"]
    assert _column(hcop_orthologs, "orth_id").nullable is False


def test_hcop_orthologs_class_a_class_b_are_mysql_enums(
    hcop_orthologs,
) -> None:
    """``class_a``/``class_b`` are MySQL ``enum('Gene','Approved')`` types.

    Unlike the PG sibling's plain ``varchar(8)``, MySQL defines these columns
    as real ``ENUM`` types. They must map to ``sqlalchemy.Enum`` — never to
    plain ``String(8)``.
    """
    for column_name in ("class_a", "class_b"):
        col = _column(hcop_orthologs, column_name)
        assert isinstance(col.type, SAEnum), column_name
        assert set(col.type.enums) == HCOPY_ENUM_VALUES, column_name
        assert col.nullable is True


def test_hcop_orthologs_has_mysql_specific_kwargs(hcop_orthologs) -> None:
    """MySQL table carries ``mysql_charset``/``mysql_collate`` kwargs."""
    table_kwargs = hcop_orthologs.__table__.kwargs
    assert table_kwargs.get("mysql_charset") == "utf8mb4"
    assert table_kwargs.get("mysql_collate") == "utf8mb4_unicode_ci"


def test_hcop_orthologs_has_declared_indexes(hcop_orthologs) -> None:
    """The dump defines 9 named indexes that must be declared."""
    indexes = {idx.name for idx in hcop_orthologs.__table__.indexes}
    expected_indexes = {
        "ho_ta_tb_idx",
        "ho_idataxa_idx",
        "ho_idbtaxb_idx",
        "ho_enstaxa_idx",
        "ho_enstaxb_idx",
        "ho_enztaxa_idx",
        "ho_enztaxb_idx",
        "ho_symtaxa_idx",
        "ho_symtaxb_idx",
    }
    assert indexes == expected_indexes


def test_hcop_orthologs_is_instantiable(hcop_orthologs) -> None:
    """The model can be instantiated with representative (NOT NULL) data."""
    row = hcop_orthologs(
        orth_id=1,
        taxon_a=9606,
        taxon_b=10090,
        db_id_a="HGNC:5",
        db_id_b="MGI:88031",
        ensembl_a="ENSG00000121410",
        ensembl_b="ENSMUSG00000017167",
        support="of,opb,phyl",
        text_link_a="http://example.org/a",
        text_link_b="http://example.org/b",
        sort_order=1,
        class_a="Gene",
        class_b="Approved",
        name_a="alpha-1-B glycoprotein",
        name_b="alpha-1-B glycoprotein",
    )
    assert row.orth_id == 1
    assert row.taxon_a == 9606
    assert row.support == "of,opb,phyl"
    assert row.class_a == "Gene"
    assert row.class_b == "Approved"
    assert row.name_a == "alpha-1-B glycoprotein"
    assert row.text_link_a == "http://example.org/a"
    assert row.sort_order == 1
