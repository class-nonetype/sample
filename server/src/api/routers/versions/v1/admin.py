from fastapi import (
    APIRouter,
    Depends,
)

from src.core.database.queries.select import select_all_user_groups
from src.core.schemas.sign_up_request import *
from src.core.database.session import database

from starlette.status import *

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


from src.core.database.queries.insert import insert_user_account


@router.post(path='/create/users')
async def post_user(session: AsyncSession = Depends(database)):
    for team in await select_all_user_groups(session=session):
        if team.description == 'Soporte':
            support_group_id = team.id

        elif team.description == 'Asesoría':
            audit_group_id = team.id

    # asesoria
    await insert_user_account(
        session=session,
        schema=SignUpRequest(
            UserProfile=UserProfile(
                full_name='gonzalo vivanco zepeda',
                email='vivanco.gm@gmail.com',
                is_active=True),
            UserAccount=UserAccount(
                username='gvivanco',
                password='12345678'),
            UserGroup=UserGroup(id=audit_group_id)
        )
    )

