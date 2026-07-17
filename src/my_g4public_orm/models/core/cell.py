"""cell model - standalone table with no foreign keys."""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class Cell(DeclarativeBase):
    """Model for the cell table.

    No real primary key in DB, cell_id is treated as the primary key
    in the ORM for CRUD operations.
    """

    __tablename__ = "cell"

    # Primary key (forced ORM PK - no real DB PK constraint)
    cell_id: Mapped[int | None] = mapped_column(Integer, primary_key=True)

    # String columns
    cell_name: Mapped[str | None] = mapped_column(String(255))
    cell_alias: Mapped[str | None] = mapped_column(String(255))
    cell_table: Mapped[str | None] = mapped_column(String(255))

    # Text columns
    cell_permit: Mapped[str | None] = mapped_column(Text)
    cell_view: Mapped[str | None] = mapped_column(Text)
    cell_edit: Mapped[str | None] = mapped_column(Text)
    cell_lint: Mapped[str | None] = mapped_column(Text)
    cell_notes: Mapped[str | None] = mapped_column(Text)

    # Integer column
    cell_sort: Mapped[int | None] = mapped_column(Integer)
