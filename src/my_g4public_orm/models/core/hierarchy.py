"""hierarchy model - family hierarchy table with composite primary key."""

from __future__ import annotations

from sqlalchemy import Index, Integer
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class Hierarchy(DeclarativeBase):
    """Model for the hierarchy table.

    Natural-composite junction table with composite primary key over the two
    joining columns (parent_fam_id, child_fam_id).
    """

    __tablename__ = "hierarchy"

    # Composite primary key
    parent_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    __table_args__ = (
        Index("hierarchy_child_fam_id_index", "child_fam_id"),
        Index("hierarchy_parent_fam_id_index", "parent_fam_id"),
    )
