"""external_resource model - external resource reference table with real primary key."""

from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class ExternalResource(DeclarativeBase):
    """Model for the external_resource table.

    Has a real primary key constraint in the database.
    """

    __tablename__ = "external_resource"

    # Primary key (real DB PK)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # String columns
    name: Mapped[str | None] = mapped_column(String(255))
    url: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))

    # Boolean column (tinyint(1) in MySQL)
    approved: Mapped[bool | None] = mapped_column(Boolean)
