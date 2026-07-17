"""locus_stats_chr model - standalone table with no foreign keys."""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class LocusStatsChr(DeclarativeBase):
    """Model for the locus_stats_chr table.

    No real primary key in DB, composite key (ls_chr, ls_type, ls_group, ls_source)
    is treated as the primary key in the ORM for CRUD operations.
    """

    __tablename__ = "locus_stats_chr"

    # Composite primary key (forced ORM PK - no real DB PK constraint)
    ls_chr: Mapped[str | None] = mapped_column(String(5), primary_key=True)
    ls_type: Mapped[str | None] = mapped_column(String(50), primary_key=True)
    ls_group: Mapped[str | None] = mapped_column(String(50), primary_key=True)
    ls_source: Mapped[str | None] = mapped_column(String(25), primary_key=True)

    # Integer columns
    ls_count: Mapped[int | None] = mapped_column(Integer)
    ls_sort: Mapped[int | None] = mapped_column(Integer)

    # String column
    ls_date: Mapped[str | None] = mapped_column(String(255))
