"""Integration schema-drift guard for ORM-vs-MySQL fidelity."""

from __future__ import annotations

from sqlalchemy import Boolean, Date, Integer, String, Text, inspect
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum
from sqlalchemy.dialects.mysql import TINYINT

from my_g4public_orm.core.base import DeclarativeBase
from my_g4public_orm.models import (
    Cell,
    Comment,
    ExternalResource,
    FamilyAlias,
    FamilyHasExternalResource,
    FamilyHasSpecialist,
    FamilyNew,
    Gencc,
    GeneHasFamily,
    HcopOrthologs,
    Hierarchy,
    HierarchyClosure,
    LocusStatsChr,
    Mane,
    PubHgnc,
    RatMusSymbol,
    Specialist,
)

ALL_MODELS: tuple[type[DeclarativeBase], ...] = (
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

EXPECTED_MODEL_PRIMARY_KEYS: dict[str, tuple[str, ...]] = {
    "cell": ("cell_id",),
    "comment": ("hgnc_id", "note"),
    "external_resource": ("id",),
    "family_alias": ("id",),
    "family_has_external_resource": ("family_id", "ext_id"),
    "family_has_specialist": ("fam_id", "specialist_id"),
    "family_new": ("id",),
    "gene_has_family": ("hgnc_id", "family_id"),
    "gencc": ("uuid",),
    "hcop_orthologs": ("orth_id",),
    "hierarchy": ("parent_fam_id", "child_fam_id"),
    "hierarchy_closure": ("parent_fam_id", "child_fam_id"),
    "locus_stats_chr": ("ls_chr", "ls_type", "ls_group", "ls_source"),
    "mane": ("id",),
    "pub_hgnc": ("gd_hgnc_id",),
    "rat_mus_symbol": ("rms_id",),
    "specialist": ("id",),
}

EXPECTED_DB_PRIMARY_KEYS: dict[str, tuple[str, ...]] = {
    "external_resource": ("id",),
    "family_new": ("id",),
    "hcop_orthologs": ("orth_id",),
    "mane": ("id",),
    "specialist": ("id",),
}

EXPECTED_HCOP_INDEXES: set[str] = {
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


def _normalize_type(column_type: object) -> tuple[str, int | tuple[str, ...] | None]:
    """Normalize reflected/model SQLAlchemy types for drift comparison."""
    if isinstance(column_type, (MySQLEnum, SAEnum)):
        return ("enum", tuple(column_type.enums))
    if isinstance(column_type, Boolean):
        return ("boolean", None)
    if isinstance(column_type, TINYINT) and column_type.display_width == 1:
        # MySQL reflects tinyint(1) for bool-like columns.
        return ("boolean", None)
    if isinstance(column_type, Text) or "TEXT" in type(column_type).__name__.upper():
        return ("text", None)
    if isinstance(column_type, Date):
        return ("date", None)
    if isinstance(column_type, String):
        return ("varchar", column_type.length)
    if isinstance(column_type, Integer):
        return ("integer", None)
    return (type(column_type).__name__.lower(), None)


def _pk_cols(model: type[DeclarativeBase]) -> tuple[str, ...]:
    return tuple(column.name for column in model.__table__.primary_key.columns)


def _index_names(model: type[DeclarativeBase]) -> set[str]:
    return {index.name for index in model.__table__.indexes if index.name is not None}


def _is_orm_only_pk_column(table_name: str, column_name: str) -> bool:
    """True when a model PK is forced in ORM metadata but absent in DB constraints."""
    model_pk = set(EXPECTED_MODEL_PRIMARY_KEYS[table_name])
    db_pk = set(EXPECTED_DB_PRIMARY_KEYS.get(table_name, ()))
    return column_name in model_pk and column_name not in db_pk


def test_schema_drift_against_reflected_mysql_schema(loaded_schema_engine) -> None:
    """Every model must match reflected table columns/types/nullability/PK/indexes."""
    inspector = inspect(loaded_schema_engine)

    expected_tables = {model.__tablename__ for model in ALL_MODELS}
    assert len(expected_tables) == 17
    assert set(inspector.get_table_names()) == expected_tables

    for model in ALL_MODELS:
        table_name = model.__tablename__

        db_columns = {row["name"]: row for row in inspector.get_columns(table_name)}
        model_columns = {column.name: column for column in model.__table__.columns}

        assert set(db_columns) == set(model_columns), (
            f"column-name drift in {table_name}: "
            f"db={sorted(db_columns)} model={sorted(model_columns)}"
        )

        for column_name, model_column in model_columns.items():
            reflected = db_columns[column_name]

            if not _is_orm_only_pk_column(table_name, column_name):
                assert reflected["nullable"] == model_column.nullable, (
                    f"nullability drift in {table_name}.{column_name}: "
                    f"db={reflected['nullable']} model={model_column.nullable}"
                )

            db_type = _normalize_type(reflected["type"])
            model_type = _normalize_type(model_column.type)
            assert db_type == model_type, (
                f"type drift in {table_name}.{column_name}: "
                f"db={db_type} model={model_type}"
            )

        reflected_pk = tuple(
            inspector.get_pk_constraint(table_name).get("constrained_columns") or ()
        )
        expected_db_pk = EXPECTED_DB_PRIMARY_KEYS.get(table_name, ())
        assert reflected_pk == expected_db_pk, (
            f"DB PK drift in {table_name}: db={reflected_pk} expected={expected_db_pk}"
        )

        expected_model_pk = EXPECTED_MODEL_PRIMARY_KEYS[table_name]
        assert _pk_cols(model) == expected_model_pk, (
            f"model PK drift in {table_name}: "
            f"model={_pk_cols(model)} expected={expected_model_pk}"
        )

        reflected_indexes = {
            index["name"] for index in inspector.get_indexes(table_name) if index.get("name")
        }
        assert reflected_indexes == _index_names(model), (
            f"index-name drift in {table_name}: "
            f"db={sorted(reflected_indexes)} model={sorted(_index_names(model))}"
        )


def test_hcop_orthologs_collation_and_indexes(loaded_schema_engine) -> None:
    """hcop_orthologs must keep its explicit collation and all 9 named indexes."""
    inspector = inspect(loaded_schema_engine)

    reflected_indexes = {
        index["name"]
        for index in inspector.get_indexes("hcop_orthologs")
        if index.get("name")
    }
    assert reflected_indexes == EXPECTED_HCOP_INDEXES

    with loaded_schema_engine.connect() as connection:
        reflected_collation = connection.exec_driver_sql(
            """
            SELECT TABLE_COLLATION
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'hcop_orthologs'
            """
        ).scalar_one()

    assert reflected_collation == "utf8mb4_unicode_ci"
