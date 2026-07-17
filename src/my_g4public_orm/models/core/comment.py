"""comment model - gene comments with composite primary key."""

from __future__ import annotations

from sqlalchemy import Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class Comment(DeclarativeBase):
    """Model for the comment table.

    DB has no PK constraint. Composite primary key (hgnc_id, note) is forced
    for ORM CRUD operations.
    """

    __tablename__ = "comment"

    # Composite primary key (forced ORM PK - no real DB PK constraint)
    # Both columns are nullable in the DB dump but forced as PK in ORM
    hgnc_id: Mapped[int | None] = mapped_column(Integer, primary_key=True)
    note: Mapped[str | None] = mapped_column(Text, primary_key=True)

    __table_args__ = (Index("comment_hgnc_id_index", "hgnc_id"),)
