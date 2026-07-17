"""pub_hgnc model - the central gene table with ~58 columns and 7 indexes."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase

if TYPE_CHECKING:
    pass


class PubHgnc(DeclarativeBase):
    """Model for the pub_hgnc table.

    DB has no PK constraint, only index. gd_hgnc_id is treated as the primary key
    in the ORM for CRUD operations.
    """

    __tablename__ = "pub_hgnc"

    # Primary key (forced ORM PK - no real DB PK constraint)
    gd_hgnc_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # String columns
    gd_app_sym: Mapped[str | None] = mapped_column(String(50))
    gd_app_sym_sort: Mapped[str | None] = mapped_column(Text)
    gd_app_name: Mapped[str | None] = mapped_column(Text)
    gd_status: Mapped[str | None] = mapped_column(String(20))
    gd_locus_type: Mapped[str | None] = mapped_column(String(100))
    gd_prev_sym: Mapped[str | None] = mapped_column(Text)
    gd_prev_name: Mapped[str | None] = mapped_column(Text)
    gd_aliases: Mapped[str | None] = mapped_column(Text)
    gd_name_aliases: Mapped[str | None] = mapped_column(Text)
    gd_pub_chrom_map: Mapped[str | None] = mapped_column(String(255))
    gd_pub_chrom_map_sort: Mapped[str | None] = mapped_column(String(255))
    gd_date2app_or_res: Mapped[date | None] = mapped_column(Date)
    gd_date_mod: Mapped[date | None] = mapped_column(Date)
    gd_date_name_change: Mapped[date | None] = mapped_column(Date)
    gd_pub_acc_ids: Mapped[str | None] = mapped_column(Text)
    gd_enz_ids: Mapped[str | None] = mapped_column(Text)
    gd_pub_eg_id: Mapped[int | None] = mapped_column(Integer)
    gd_mgd_id: Mapped[str | None] = mapped_column(Text)
    gd_other_ids: Mapped[str | None] = mapped_column(Text)
    gd_other_ids_list: Mapped[str | None] = mapped_column(Text)
    gd_pubmed_ids: Mapped[str | None] = mapped_column(Text)
    gd_pub_refseq_ids: Mapped[str | None] = mapped_column(Text)
    gd_gene_fam_name: Mapped[str | None] = mapped_column(Text)
    gd_gene_fam_pagename: Mapped[str | None] = mapped_column(Text)
    gd_date_sym_change: Mapped[date | None] = mapped_column(Date)
    gd_record_type: Mapped[str | None] = mapped_column(Text)
    gd_primary_ids: Mapped[str | None] = mapped_column(Text)
    gd_secondary_ids: Mapped[str | None] = mapped_column(Text)
    gd_pub_hseq_id: Mapped[str | None] = mapped_column(String(255))
    gd_pub_hseq_seq: Mapped[str | None] = mapped_column(Text)
    gd_pub_hseq_molecule: Mapped[str | None] = mapped_column(Text)
    gd_vega_ids: Mapped[str | None] = mapped_column(String(18))
    gd_lsdb_links: Mapped[str | None] = mapped_column(Text)
    gd_pub_ensembl_id: Mapped[str | None] = mapped_column(String(15))
    gd_ccds_ids: Mapped[str | None] = mapped_column(Text)
    gd_locus_group: Mapped[str | None] = mapped_column(Text)
    gd_cust_sort: Mapped[str | None] = mapped_column(String(255))
    gd_gene_fam_links: Mapped[str | None] = mapped_column(Text)
    gd_coord: Mapped[str | None] = mapped_column(Text)
    md_gdb_id: Mapped[str | None] = mapped_column(String(255))
    md_eg_id: Mapped[int | None] = mapped_column(Integer)
    md_mim_id: Mapped[str | None] = mapped_column(String(255))
    md_refseq_id: Mapped[str | None] = mapped_column(String(255))
    md_prot_id: Mapped[str | None] = mapped_column(Text)
    md_ensembl_id: Mapped[str | None] = mapped_column(String(15))
    md_vega_id: Mapped[str | None] = mapped_column(String(18))
    md_rna_central_ids: Mapped[str | None] = mapped_column(Text)
    md_lncipedia: Mapped[str | None] = mapped_column(String(15))
    md_gtrnadb: Mapped[str | None] = mapped_column(String(20))
    md_ucsc_id: Mapped[str | None] = mapped_column(String(50))
    md_rgd_id: Mapped[str | None] = mapped_column(String(50))
    md_mgd_id: Mapped[str | None] = mapped_column(Text)
    md_agr: Mapped[int | None] = mapped_column(Integer)
    md_alphafold: Mapped[str | None] = mapped_column(Text)

    # Boolean columns (tinyint(1) in MySQL)
    gd_ambiguous: Mapped[bool | None] = mapped_column(Boolean)
    gd_to_review: Mapped[bool | None] = mapped_column(Boolean)
    gd_stable_symbol: Mapped[bool | None] = mapped_column(Boolean)

    __table_args__ = (
        Index("pub_hgnc_gd_app_sym_index", "gd_app_sym"),
        Index("pub_hgnc_gd_hgnc_id_index", "gd_hgnc_id"),
        Index("pub_hgnc_gd_pub_eg_id_index", "gd_pub_eg_id"),
        Index("pub_hgnc_gd_pub_ensembl_id_index", "gd_pub_ensembl_id"),
        Index("pub_hgnc_md_eg_id_index", "md_eg_id"),
        Index("pub_hgnc_md_ensembl_id_index", "md_ensembl_id"),
        Index("pub_hgnc_md_vega_id_index", "md_vega_id"),
    )
