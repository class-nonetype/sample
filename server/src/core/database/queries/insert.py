from __future__ import annotations


from bcrypt import gensalt, hashpw
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.queries.helpers import insert_object_model
from src.core.database.models import *


from src.core.schemas.sign_up_request import SignUpRequest




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

