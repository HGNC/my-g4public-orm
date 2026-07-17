"""``gene_has_family`` ORM model."""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class GeneHasFamily(DeclarativeBase):
    """Junction linking an HGNC gene to a family."""

    __tablename__ = "gene_has_family"

    hgnc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    family_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str | None] = mapped_column(String(255))
    custom_sort: Mapped[str | None] = mapped_column(String(255))
