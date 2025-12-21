from __future__ import annotations

from typing import Literal
from uuid import UUID

from sqlalchemy import and_, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.database.models import *




async def select_user_by_username(session: AsyncSession, username: str) -> UserAccounts | None:
    statement = (
        select(UserAccounts)
        .select_from(UserAccounts)
        .options(
            joinedload(UserAccounts.user_profile_relationship),
            joinedload(UserAccounts.user_group_relationship),
        )
        .where(and_(UserAccounts.username == username, UserAccounts.active == True))  # noqa: E712
    )
    result = await session.execute(statement)
    return result.scalars().first()


async def select_user_by_user_account_id(
    session: AsyncSession,
    user_account_id: UUID,
) -> UserAccounts | None:
    statement = (
        select(UserAccounts)
        .select_from(UserAccounts)
        .where(and_(UserAccounts.id == user_account_id, UserAccounts.active == True))
    )
    result = await session.execute(statement)
    return result.scalars().first()

async def select_user_group_by_user_account_id(
    session: AsyncSession,
    user_account_id: UUID,
) -> UserGroups | None:
    statement = (
        select(UserGroups)
        .select_from(UserAccounts)
        .join(UserGroups, UserGroups.id == UserAccounts.user_group_id)
        .where(UserAccounts.id == user_account_id)
        .correlate(None)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def select_user_group_name_by_user_account_id(
    session: AsyncSession,
    user_account_id: UUID,
) -> str | None:
    statement = (
        select(UserGroups.description)
        .select_from(UserAccounts)
        .join(UserGroups, UserGroups.id == UserAccounts.user_group_id)
        .where(UserAccounts.id == user_account_id)
        .correlate(None)
    )
    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def select_username_by_user_account_id(
    session: AsyncSession,
    user_account_id: UUID,
) -> str | None:
    statement = (
        select(UserAccounts.username)
        .select_from(UserAccounts)
        .where(and_(UserAccounts.id == user_account_id, UserAccounts.active == True))
    )
    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def select_user_full_name_by_user_account_id(session: AsyncSession, user_account_id) -> str | None:
    statement = (
        select(UserProfiles.full_name)
        .select_from(UserAccounts)
        .join(UserProfiles, UserProfiles.id == UserAccounts.user_profile_id)
        .where(UserAccounts.id == user_account_id)
        .correlate(None)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def select_user_profile_by_user_account_id(session: AsyncSession, user_account_id: UUID) -> UserProfiles:
    statement = (
        select(UserProfiles)
        .select_from(UserAccounts)
        .join(UserProfiles, UserProfiles.id == UserAccounts.user_profile_id)
        .where(UserAccounts.id == user_account_id)
        .correlate(None)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def select_user_email_by_user_account_id(
    session: AsyncSession, user_account_id: UUID
) -> str | None:

    statement = (
        select(UserProfiles.email)
        .select_from(UserAccounts)
        .join(UserProfiles, UserProfiles.id == UserAccounts.user_profile_id)
        .where(UserAccounts.id == user_account_id)
        .correlate(None)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def validate_user_authentication(
    session: AsyncSession,
    username: str,
    password: str,
) -> UserAccounts | Literal[False]:
    user_account = await select_user_by_username(session=session, username=username)

    if not user_account or not user_account.verify_password(password) or not user_account.active:
        return False

    return user_account


async def select_all_user_groups(
    session: AsyncSession
) -> UserGroups | None:
    statement = (
        select(UserGroups)
        .select_from(UserGroups)
    )
    result = await session.execute(statement)
    return result.scalars().all()



