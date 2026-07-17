"""family_alias model - family alias table with forced ORM primary key."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase

if TYPE_CHECKING:
    pass


class FamilyAlias(DeclarativeBase):
    """Model for the family_alias table.

    DB has no PK constraint. id is treated as the primary key
    in the ORM for CRUD operations.
    """

    __tablename__ = "family_alias"

    # Primary key (forced ORM PK - no real DB PK constraint)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Other columns
    family_id: Mapped[int | None] = mapped_column(Integer)
    alias: Mapped[str | None] = mapped_column(String(255))
