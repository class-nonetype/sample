from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, String, Text, Integer, DateTime, ForeignKey, Index, event
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.database.base import Base
from src.core.database.models.user_accounts import UserAccounts
# from src.core.database.models.team import Teams  # o Groups, según tu modelo


class UserGroups(Base):
    __tablename__ = "user_groups"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
        index=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    user_account_relationship: Mapped["UserAccounts"] = relationship(
        back_populates="user_group_relationship",
        uselist=False,
    )




@event.listens_for(UserGroups.__table__, "after_create")
def seed_default_status_types(target, connection, **kwargs) -> None:
    data = [
        {"id": uuid.uuid4(), "description": "Soporte"},
        {"id": uuid.uuid4(), "description": "Asesoría"},
    ]
    connection.execute(target.insert(), data)
