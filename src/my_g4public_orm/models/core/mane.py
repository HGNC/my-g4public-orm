"""mane model - MANE gene records with real primary key."""

from __future__ import annotations

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class Mane(DeclarativeBase):
    """Model for the mane table.

    Has a real primary key constraint in the database.
    """

    __tablename__ = "mane"

    # Primary key (real DB PK)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Other columns (exactly 7 total)
    ncbi_gene_id: Mapped[int] = mapped_column(Integer)
    ensembl_gene: Mapped[str] = mapped_column(String(20))
    hgnc_id: Mapped[int | None] = mapped_column(Integer)
    refseq_nuc_acc: Mapped[str] = mapped_column(String(20))
    ensembl_nuc_acc: Mapped[str] = mapped_column(String(20))
    mane_status: Mapped[str] = mapped_column(String(30))

    __table_args__ = (Index("mane_hgnc_id_index", "hgnc_id"),)
