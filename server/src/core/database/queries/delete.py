
from __future__ import annotations

from typing import Literal
from uuid import UUID

from sqlalchemy import and_, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.database.models import *




async def delete_ticket_by_ticket_id(
    session: AsyncSession,
    ticket_id: UUID,
):
    ticket = await session.get(Tickets, ticket_id)
    if ticket is None:
        return None

    try:
        await session.delete(ticket)
        await session.commit()
        return True
    except Exception:
        await session.rollback()
        return False
