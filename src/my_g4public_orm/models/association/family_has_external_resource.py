"""``family_has_external_resource`` ORM model."""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class FamilyHasExternalResource(DeclarativeBase):
    """Junction linking a curated family to an external resource."""

    __tablename__ = "family_has_external_resource"

    family_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ext_id: Mapped[int] = mapped_column(Integer, primary_key=True)
