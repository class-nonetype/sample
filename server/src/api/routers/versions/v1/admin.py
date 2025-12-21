from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)

from src.core.database.models.types import RequestTypes
from src.core.database.queries.helpers import insert_object_model
from src.core.database.queries.select import select_all_user_groups
from src.core.schemas.sign_up_request import *
from src.api.responses import response
from src.utils.controls import MEDIA_TYPE
from src.core.database.session import database
from src.utils.logger import logger

from starlette.status import *

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

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
                full_name='mariel andrea pineda soto',
                email='mpineda@consejodeauditoria.gob.cl',
                is_active=True),
            UserAccount=UserAccount(
                username='mpineda',
                password='12345678'),
            UserGroup=UserGroup(id=audit_group_id)
        )
    )

    await insert_user_account(
        session=session,
        schema=SignUpRequest(
            UserProfile=UserProfile(
                full_name='valentina paz perez meza',
                email='vperez@consejodeauditoria.gob.cl',
                is_active=True),
            UserAccount=UserAccount(
                username='vperez',
                password='12345678'),
            UserGroup=UserGroup(id=audit_group_id)
        )
    )
    
    await insert_user_account(
        session=session,
        schema=SignUpRequest(
            UserProfile=UserProfile(
                full_name='cesar antonio duran carvajal',
                email='cduran@consejodeauditoria.gob.cl',
                is_active=True),
            UserAccount=UserAccount(
                username='cduran',
                password='12345678'),
            UserGroup=UserGroup(id=audit_group_id)
        )
    )
    

    # soporte
    await insert_user_account(
        session=session,
        schema=SignUpRequest(
            UserProfile=UserProfile(
                full_name='francisco daniel tralma riquelme',
                email='ftralma@consejodeauditoria.gob.cl',
                is_active=True),
            UserAccount=UserAccount(
                username='ftralma',
                password='12345678'),
            UserGroup=UserGroup(id=support_group_id)
        )
    )

    await insert_user_account(
        session=session,
        schema=SignUpRequest(
            UserProfile=UserProfile(
                full_name='luis osorio rubilar',
                email='losorio@consejodeauditoria.gob.cl',
                is_active=True),
            UserAccount=UserAccount(
                username='losorio',
                password='12345678'),
            UserGroup=UserGroup(id=support_group_id)
        )
    )

    await insert_user_account(
        session=session,
        schema=SignUpRequest(
            UserProfile=UserProfile(
                full_name='gonzalo mauricio vivanco zepeda',
                email='gvivanco@consejodeauditoria.gob.cl',
                is_active=True),
            UserAccount=UserAccount(
                username='gvivanco',
                password='12345678'),
            UserGroup=UserGroup(id=support_group_id)
        )
    )


