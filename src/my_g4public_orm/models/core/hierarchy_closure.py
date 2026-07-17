"""hierarchy_closure model - family hierarchy closure table with composite primary key."""

from __future__ import annotations

from sqlalchemy import Index, Integer
from sqlalchemy.orm import Mapped, mapped_column

from my_g4public_orm.core.base import DeclarativeBase


class HierarchyClosure(DeclarativeBase):
    """Model for the hierarchy_closure table.

    Natural-composite junction table with composite primary key over the two
    joining columns (parent_fam_id, child_fam_id) - 2 cols only.
    distance is a plain nullable column, NOT part of the PK.
    """

    __tablename__ = "hierarchy_closure"

    # Composite primary key (2 cols only - unlike the PG sibling's 3-col PK)
    parent_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_fam_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Plain nullable column (NOT part of the PK)
    distance: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (
        Index("hierarchy_closure_child_fam_id_index", "child_fam_id"),
        Index("hierarchy_closure_parent_fam_id_index", "parent_fam_id"),
    )
