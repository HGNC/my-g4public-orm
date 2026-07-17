"""family_new model - family group table with real primary key."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase

if TYPE_CHECKING:
    pass


class FamilyNew(DeclarativeBase):
    """Model for the family_new table.

    Has a real primary key constraint in the database.
    """

    __tablename__ = "family_new"

    # Primary key (real DB PK)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # String columns
    abbreviation: Mapped[str | None] = mapped_column(String(50))
    name: Mapped[str | None] = mapped_column(String(150))
    editor: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str | None] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(50))
    desc_label: Mapped[str | None] = mapped_column(String(255))
    desc_source: Mapped[str | None] = mapped_column(String(255))
    desc_go: Mapped[str | None] = mapped_column(String(255))
    typical_gene: Mapped[str | None] = mapped_column(String(255))

    # Text columns
    curator_comment: Mapped[str | None] = mapped_column(Text)
    external_note: Mapped[str | None] = mapped_column(Text)
    pubmed_ids: Mapped[str | None] = mapped_column(Text)
    desc_comment: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("family_new_abbreviation_index", "abbreviation"),
        Index("family_new_name_index", "name"),
    )
