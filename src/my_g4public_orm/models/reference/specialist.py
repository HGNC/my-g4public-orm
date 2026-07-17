"""specialist model - specialist reference table with real primary key."""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class Specialist(DeclarativeBase):
    """Model for the specialist table.

    Has a real primary key constraint in the database.
    """

    __tablename__ = "specialist"

    # Primary key (real DB PK)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # String columns
    name: Mapped[str | None] = mapped_column(String(255))
    url: Mapped[str | None] = mapped_column(String(255))

    # Text column
    address: Mapped[str | None] = mapped_column(Text)
