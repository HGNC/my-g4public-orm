"""``family_has_specialist`` ORM model."""

from __future__ import annotations

from sqlalchemy import Index, Integer
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class FamilyHasSpecialist(DeclarativeBase):
    """Junction linking a curated family to a specialist page."""

    __tablename__ = "family_has_specialist"

    fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    specialist_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    __table_args__ = (
        Index("family_has_specialist_fam_id_index", "fam_id"),
        Index("family_has_specialist_specialist_id_index", "specialist_id"),
    )
