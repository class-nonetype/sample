from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, String, Text, Integer, DateTime, ForeignKey, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.database.base import Base
from src.core.database.models import *


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )

    name: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    path: Mapped[str] = mapped_column(Text, nullable=False, index=True)

    priority_type_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("priority_types.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # encargado
    manager_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_accounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    group_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_groups.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


    priority_relationship: Mapped["PriorityTypes"] = relationship(
        "PriorityTypes",
        foreign_keys=[priority_type_id],
    )

    manager_relationship: Mapped["UserAccounts"] = relationship(
        "UserAccounts",
        foreign_keys=[manager_id],
    )

    group_relationship: Mapped["UserGroups"] = relationship(
        "UserGroups",
        foreign_keys=[group_id],
    )
