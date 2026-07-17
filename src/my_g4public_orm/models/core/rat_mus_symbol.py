"""rat_mus_symbol model - rat/mouse symbol mappings with forced ORM primary key."""

from __future__ import annotations

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class RatMusSymbol(DeclarativeBase):
    """Model for the rat_mus_symbol table.

    DB has no PK constraint. rms_id is treated as the primary key in the ORM
    for CRUD operations.
    """

    __tablename__ = "rat_mus_symbol"

    # Primary key (forced ORM PK - no real DB PK constraint)
    # Column is nullable in the DB dump but forced as PK in ORM
    rms_id: Mapped[str | None] = mapped_column(String(25), primary_key=True)

    # Other columns
    rms_sym: Mapped[str | None] = mapped_column(String(25))
    rms_hgnc_id: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (Index("rat_mus_symbol_rms_id_index", "rms_id"),)
