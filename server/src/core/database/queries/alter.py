from __future__ import annotations

from uuid import UUID

from sqlalchemy import and_, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.queries.select import select_status_type_description_by_id
from src.core.database.models.types import StatusTypes
from src.core.database.models.tickets import Tickets
from src.core.database.models import UserAccounts
from src.utils.time import get_datetime
from src.utils.logger import logger

async def update_last_login_date(session: AsyncSession, user_account_id: UUID) -> bool:
    try:
        stmt = (
            update(UserAccounts)
            .where(and_(UserAccounts.id == user_account_id, UserAccounts.active == True))  # noqa: E712
            .values(last_login_date=get_datetime())
        )
        await session.execute(stmt)
        await session.commit()
        return True
    except Exception:  # pylint: disable=broad-except
        await session.rollback()
        return False



async def update_ticket(
    session: AsyncSession,
    context: str,
    ticket_id: UUID,
    object_id: UUID | None = None,
    resolution: str | None = None,
    is_resolved: bool | None = None,
) -> tuple[bool | None, Tickets | None]:
    async def select_ticket_by_ticket_id(session: AsyncSession, ticket_id: UUID) -> Tickets | None:
        ticket_query = (
            select(Tickets)
            .where(Tickets.id == ticket_id)
            .limit(1)
        )
        result = await session.execute(ticket_query)
        return result.scalars().first()
    
    
    try:
        match context:
            case 'status':
                ticket_object_model = await select_ticket_by_ticket_id(session=session, ticket_id=ticket_id)
                if not ticket_object_model:
                    return None, None

                new_status_description = await select_status_type_description_by_id(session, object_id)
                update_values = {
                    'status_type_id': object_id,
                    'updated_at': get_datetime(),
                }

                # No marcar como resuelto automaticamente; queda en espera de feedback.
                if new_status_description == 'Resuelto':
                    update_values['is_resolved'] = None
                    update_values['resolved_at'] = None

                statement = (
                    update(Tickets)
                    .where(Tickets.id == ticket_id, Tickets.is_active.is_(True))
                    .values(**update_values)
                )

                await session.execute(statement)
                await session.commit()

                ticket_object_model = await select_ticket_by_ticket_id(session=session, ticket_id=ticket_id)
                return True, ticket_object_model


            case 'manager':
                # estado 'En proceso'
                status_query = (
                    select(StatusTypes.id)
                    .where(
                        StatusTypes.description.is_not(None),
                        func.lower(StatusTypes.description) == 'en proceso'
                    )
                    .limit(1)
                )

                result = await session.execute(status_query)
                status_id = result.scalar_one_or_none()

                if not status_id:
                    return None, None

                statement = (
                    update(Tickets)
                    .where(Tickets.id == ticket_id, Tickets.is_active.is_(True))
                    .values(
                        manager_id=object_id,
                        status_type_id=status_id,
                        updated_at=get_datetime())
                )

                await session.execute(statement)
                await session.commit()

                ticket_object_model = await select_ticket_by_ticket_id(session=session, ticket_id=ticket_id)
                return True, ticket_object_model


            case 'read':
                statement = (
                    update(Tickets)
                    .where(Tickets.id == ticket_id, Tickets.is_readed.is_(False))
                    .values(is_readed=True, updated_at=get_datetime())
                )

                await session.execute(statement)
                await session.commit()

                ticket_object_model = await select_ticket_by_ticket_id(session=session, ticket_id=ticket_id)
                return True, ticket_object_model


            case 'resolved':
                print(f'resolviendo...')
                ticket_object_model = await select_ticket_by_ticket_id(session=session, ticket_id=ticket_id)
                if not ticket_object_model or is_resolved is None:
                    return None, None

                statement = (
                    update(Tickets)
                    .where(Tickets.id == ticket_id, Tickets.is_active.is_(True))
                    .values(
                        is_resolved=is_resolved,
                        resolved_at=get_datetime() if is_resolved else None,
                        updated_at=get_datetime(),
                    )
                )

                await session.execute(statement)
                await session.commit()

                ticket_object_model = await select_ticket_by_ticket_id(session=session, ticket_id=ticket_id)
                return True, ticket_object_model


            case 'resolution':
                statement = (
                    update(Tickets)
                    .where(Tickets.id == ticket_id, Tickets.is_active.is_(True))
                    .values(resolution=resolution, updated_at=get_datetime())
                )

                await session.execute(statement)
                await session.commit()

                ticket_object_model = await select_ticket_by_ticket_id(session=session, ticket_id=ticket_id)
                return True, ticket_object_model

    except Exception as exception:
        logger.exception(msg=exception)
        await session.rollback()
        return False, None
