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


class ProjectNodes(Base):
    __tablename__ = "project_nodes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )
    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    name: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    path: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    
    # tipo: 'folder' o 'file' (si quieres, cambia a Enum)
    node_type: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default='folder',
        server_default='folder',
        index=True,
    )
    


    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


    parent_relationship: Mapped["Projects"] = relationship(
        "Projects",
        foreign_keys=[parent_id],
    )

