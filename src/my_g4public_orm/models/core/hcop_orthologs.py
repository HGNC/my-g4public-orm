"""``hcop_orthologs`` ORM model — HCOP pairwise ortholog records.

Maps the existing ``g4public.hcop_orthologs`` schema (MySQL). Column types
and nullability are transcribed verbatim from the authoritative Navicat dump
``.ai/specs/my-g4public.sql``. The ORM reads and writes **data only** — it
never creates, alters, or drops schema objects (``primary_key=True`` emits no
DDL).

The dump defines a real database primary key on ``orth_id`` (``int
AUTO_INCREMENT``); per the primary-key convention it is the ORM primary key
(emits no DDL). ``class_a``/``class_b`` are MySQL ``enum('Gene','Approved')``
types — **NOT** ``varchar(8)`` like the PG sibling.
"""

from __future__ import annotations

from sqlalchemy import Enum as SAEnum
from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class HcopOrthologs(DeclarativeBase):
    """HCOP (HCOP Comparison of Orthology Predictions) pairwise ortholog row.

    ``orth_id`` (real DB PK, AUTO_INCREMENT) is the ORM primary key.
    ``taxon_a``/``taxon_b``/``sort_order`` are ``int`` -> ``Integer``;
    ``class_a``/``class_b`` are MySQL ``ENUM`` types (unlike PG's varchar);
    ``name_a``/``name_b``/``text_link_a``/``text_link_b`` are ``mediumtext`` -> ``Text``.
    The NOT NULL columns are ``orth_id``, ``taxon_a``/``taxon_b``, ``db_id_a``/``db_id_b``,
    ``ensembl_a``/``ensembl_b``, ``support``, ``text_link_a``/``text_link_b``
    and ``sort_order``. ``class_a``/``class_b`` are nullable enums.

    The table carries MySQL-specific dialect options:
    ``mysql_charset="utf8mb4"``, ``mysql_collate="utf8mb4_unicode_ci"``.
    """

    __tablename__ = "hcop_orthologs"

    # MySQL-specific table arguments
    __table_args__ = (
        Index("ho_ta_tb_idx", "taxon_a", "taxon_b"),
        Index("ho_idataxa_idx", "db_id_a", "taxon_a"),
        Index("ho_idbtaxb_idx", "db_id_b", "taxon_b"),
        Index("ho_enstaxa_idx", "ensembl_a", "taxon_a"),
        Index("ho_enstaxb_idx", "ensembl_b", "taxon_b"),
        Index("ho_enztaxa_idx", "entrez_a", "taxon_a"),
        Index("ho_enztaxb_idx", "entrez_b", "taxon_b"),
        Index("ho_symtaxa_idx", "symbol_a", "taxon_a"),
        Index("ho_symtaxb_idx", "symbol_b", "taxon_b"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

    # --- Primary key (real DB PK, AUTO_INCREMENT) ---
    orth_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # --- Taxonomy (int -> Integer, NOT NULL) ---
    taxon_a: Mapped[int] = mapped_column(Integer, nullable=False)
    taxon_b: Mapped[int] = mapped_column(Integer, nullable=False)

    # --- Cross-database identifiers ---
    db_id_a: Mapped[str] = mapped_column(String(10), nullable=False)
    db_id_b: Mapped[str] = mapped_column(String(25), nullable=False)
    vgnc_a: Mapped[str | None] = mapped_column(String(28))
    vgnc_b: Mapped[str | None] = mapped_column(String(28))
    ensembl_a: Mapped[str] = mapped_column(String(28), nullable=False)
    ensembl_b: Mapped[str] = mapped_column(String(28), nullable=False)
    entrez_a: Mapped[str | None] = mapped_column(String(28))
    entrez_b: Mapped[str | None] = mapped_column(String(28))

    # --- Symbol + gene names ---
    symbol_a: Mapped[str | None] = mapped_column(String(25))
    symbol_b: Mapped[str | None] = mapped_column(String(40))
    symbol_source_a: Mapped[str | None] = mapped_column(String(128))
    symbol_source_b: Mapped[str | None] = mapped_column(String(128))
    name_a: Mapped[str | None] = mapped_column(Text)  # mediumtext -> Text
    name_b: Mapped[str | None] = mapped_column(Text)  # mediumtext -> Text

    # --- Source / locus metadata ---
    source_name_a: Mapped[str | None] = mapped_column(String(128))
    source_name_b: Mapped[str | None] = mapped_column(String(128))
    locus_type_a: Mapped[str | None] = mapped_column(String(255))
    locus_type_b: Mapped[str | None] = mapped_column(String(255))
    locus_source_a: Mapped[str | None] = mapped_column(String(128))
    locus_source_b: Mapped[str | None] = mapped_column(String(128))

    # --- class_a / class_b: MySQL ENUM (not varchar like PG) ---
    class_a: Mapped[str | None] = mapped_column(SAEnum("Gene", "Approved"))
    class_b: Mapped[str | None] = mapped_column(SAEnum("Gene", "Approved"))

    # --- Chromosomes / support / links ---
    chr_a: Mapped[str | None] = mapped_column(String(128))
    chr_b: Mapped[str | None] = mapped_column(String(128))
    support: Mapped[str] = mapped_column(String(255), nullable=False)
    text_link_a: Mapped[str] = mapped_column(Text, nullable=False)  # mediumtext -> Text
    text_link_b: Mapped[str] = mapped_column(Text, nullable=False)  # mediumtext -> Text
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
