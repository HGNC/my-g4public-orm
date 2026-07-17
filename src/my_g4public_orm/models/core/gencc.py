"""gencc model - gene-disease associations with UUID primary key."""

from __future__ import annotations

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class Gencc(DeclarativeBase):
    """Model for the gencc table.

    DB has no PK constraint. uuid is treated as the primary key in the ORM
    for CRUD operations.
    """

    __tablename__ = "gencc"

    # Primary key (forced ORM PK - no real DB PK constraint)
    uuid: Mapped[str] = mapped_column(String(255), primary_key=True)

    # Other columns
    hgnc_id: Mapped[int | None] = mapped_column(Integer)
    disease_id: Mapped[str | None] = mapped_column(String(255))
    disease_title: Mapped[str | None] = mapped_column(String(255))
    omim_id: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (Index("gencc_hgnc_id_index", "hgnc_id"),)
