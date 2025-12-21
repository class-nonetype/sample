from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.encoders import jsonable_encoder


from src.core.schemas.sign_up_request import *
from src.api.responses import response
from src.utils.controls import MEDIA_TYPE
from src.core.database.session import database

from starlette.status import *

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()




@router.get(path='/health-check')
async def health_check(session: AsyncSession = Depends(database)):
    return response(
        response_type=2,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        media_type=MEDIA_TYPE,
        content=jsonable_encoder(obj={
            'status': 'error',
            'message': 'Database session could not be established.'
        })
    ) if not session else response(
        response_type=2,
        status_code=status.HTTP_200_OK,
        media_type=MEDIA_TYPE,
        content=jsonable_encoder(obj={
            'status': 'ok',
            'message': 'Service is healthy and operational.'
        })
    )

