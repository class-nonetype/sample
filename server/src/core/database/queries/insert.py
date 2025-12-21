from __future__ import annotations


from bcrypt import gensalt, hashpw
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.queries.helpers import insert_object_model
from src.core.database.models import *


from src.core.schemas.project_request import ProjectRequest

from src.utils.paths import get_project_directory_path

from src.core.schemas.sign_up_request import SignUpRequest


async def inser_project(session: AsyncSession, schema: ProjectRequest) -> Projects:
    
    return await insert_object_model(
        session=session,
        base_model=Projects,
        data_model={
            'id': schema.id,
            'name': schema.name.strip().upper(),
            'path': get_project_directory_path(schema.id),
            'priority_type_id': schema.priority_type_id,
            'manager_id': schema.manager_id,
            'group_id': schema.group_id,
        }
    )




async def insert_user_account(session: AsyncSession, schema: SignUpRequest) -> dict | bool:
    user_profile = await insert_object_model(
        session=session,
        base_model=UserProfiles,
        data_model={
            'full_name': schema.UserProfile.full_name.upper(),
            'email': schema.UserProfile.email
        }
    )

    user_account = await insert_object_model(
        session=session,
        base_model=UserAccounts,
        data_model={
            'user_profile_id': user_profile.id,
            'user_group_id': schema.UserGroup.id,
            'username': schema.UserAccount.username,
            'password': hashpw(schema.UserAccount.password.encode("utf-8"), gensalt()).decode("utf-8"),
        }
    )

    return {
        'userProfileId': user_account.user_profile_id,
        'userGroupId': user_account.user_group_id,
        'username': user_account.username,
    }

'''

async def insert_user_account(session: AsyncSession, schema: SignUpRequest) -> dict | bool:
    try:
        user_profile = UserProfiles(
            full_name=schema.UserProfile.full_name.upper(),
            email=schema.UserProfile.email
        )
        session.add(user_profile)
        try:
            await session.flush()

        except IntegrityError:
            await session.rollback()
            raise

        await session.commit()
        await session.refresh(user_profile)

        user_account = UserAccounts(
            user_profile_id=user_profile.id,
            group_id=schema.TeamGroup.id,
            username=schema.UserAccount.username,
            password=hashpw(schema.UserAccount.password.encode("utf-8"), gensalt()).decode("utf-8"),
        )

        session.add(user_account)
        try:
            await session.flush()

        except IntegrityError:
            await session.rollback()
            raise

        await session.commit()
        await session.refresh(user_account)

        return {
            "userProfileId": user_account.user_profile_id,
            "teamGroupId": user_account.group_id,
            "username": user_account.username,
        }

    except Exception as exception:  # pylint: disable=broad-except
        await session.rollback()
        logger.error(msg=exception)
        return False




async def insert_user_role(
    session: AsyncSession,
    value: str | None = None,
    description: str | None = None,
    payload=None,
) -> dict | bool:
    try:
        if payload is not None:
            value = getattr(payload, "value", value)
            description = getattr(payload, "description", description)

        if value is None:
            raise ValueError("User role value is required")

        user_role = UserRoles(
            id=generate_uuid_v4(),
            value=value,
            description=description,
        )

        session.add(user_role)
        await session.commit()
        await session.refresh(user_role)

        return {
            "id": user_role.id,
            "value": user_role.value,
            "description": user_role.description,
        }
    except Exception as exception:  # pylint: disable=broad-except
        await session.rollback()
        logger.error(msg=exception)
        return False
'''
