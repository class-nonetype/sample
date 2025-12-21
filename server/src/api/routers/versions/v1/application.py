from datetime import datetime, timedelta
from pathlib import Path
from uuid import UUID, uuid4
from typing import Annotated

from collections.abc import AsyncGenerator, Sequence

from pydantic import EmailStr
from starlette.status import *

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
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.project_request import ProjectRequest
from src.core.database.queries.delete import delete_ticket_by_ticket_id
from src.core.services import send_email
from src.api.responses import response
from src.core.schemas.ticket_request import TicketRequest

from src.core.database.queries.insert import insert_project, insert_ticket
from src.core.database.queries.helpers import insert_object_model
from src.core.database.session import database


from src.core.database.queries.alter import update_ticket
from src.core.database.queries.select import (
    select_all_tickets_by_requester_id,
    select_all_tickets_for_manager,
    select_count_tickets_by_requester_id,
    select_count_tickets_for_manager,
    select_all_request_types,
    select_all_priority_types,
    select_all_status_types,
    select_all_user_groups,
    select_all_support_users,
    select_status_type_description_by_id,
    select_ticket_attachment_by_id,
    select_request_type_description_by_id,
    select_user_emails,
    select_ticket_by_id,
)
from src.core.database.models import TicketAttachments
from src.utils.paths import TICKETS_ATTACHMENTS_DIRECTORY_PATH

from src.api.routers.versions.v1.web_socket import broadcast
from src.utils.logger import logger
from src.utils.formats import (
    build_ticket_email_body,
    build_ticket_email_text,
    build_ticket_status_email_body,
    build_ticket_status_email_text,
)
router = APIRouter()


@router.post(path='/create/project')
async def post_project(
    request: Request,
    session: Annotated[AsyncSession, Depends(database)],
    name: str = Form(''),

    group_id: UUID | None = Form(None),
    priority_type_id: UUID = Form(...),
    manager_id: UUID = Form(...),

):
    
    object_model = await insert_project(
        session=session,
        schema=ProjectRequest(
            id=uuid4(),
            name=name,
            group_id=group_id,
            priority_type_id=priority_type_id,
            manager_id=manager_id,
        )
    )
    
    if not object_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No se pudo crear el proyecto')
    
    
    return response(response_type=1, status_code=HTTP_201_CREATED)



@router.post(path='/create/ticket', status_code=status.HTTP_201_CREATED)
async def post_ticket(
    request: Request,
    session: Annotated[AsyncSession, Depends(database)],
    code: str = Form(...),
    note: str = Form(''),
    request_type_id: UUID = Form(...),
    priority_type_id: UUID = Form(...),
    status_type_id: UUID = Form(...),
    requester_id: UUID = Form(...),
    group_id: UUID | None = Form(None),
    due_at: str | None = Form(None),
    resolved_at: str | None = Form(None),
    closed_at: str | None = Form(None),
    attachments: (UploadFile | list[UploadFile] | Sequence[UploadFile] | None) = File(None),
):

    ticket_object_model = await insert_ticket(
        session=session,
        schema=TicketRequest(
            code=code,
            note=note,
            request_type_id=request_type_id,
            priority_type_id=priority_type_id,
            status_type_id=status_type_id,
            requester_id=requester_id,
            group_id=group_id,
            due_at=due_at,
            resolved_at=resolved_at,
            closed_at=closed_at,
        )
    )
    if not ticket_object_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No se pudo crear el ticket')
    

    # Normaliza a lista incluso cuando FastAPI entrega un solo UploadFile.
    if attachments is None:
        ticket_attachment_uploads: list[UploadFile] = []
    elif isinstance(attachments, (list, tuple)):
        ticket_attachment_uploads = [uploaded_file for uploaded_file in attachments if uploaded_file is not None]
    else:
        ticket_attachment_uploads = [attachments]
    if len(ticket_attachment_uploads) > 0:
        ticket_attachment_directory_path = Path(TICKETS_ATTACHMENTS_DIRECTORY_PATH / str(ticket_object_model.id))
        ticket_attachment_directory_path.mkdir(parents=True, exist_ok=True)

        for ticket_attachment_upload in ticket_attachment_uploads:
            ticket_attachment_upload: UploadFile

            ticket_attachment_upload_file_name = Path(ticket_attachment_upload.filename).name
            if not ticket_attachment_upload_file_name:
                ticket_attachment_upload.file.close()
                continue

            ticket_attachment_upload_file_content = await ticket_attachment_upload.read()
            ticket_attachment_upload_file_uuid_name = f'{uuid4().hex}{Path(ticket_attachment_upload_file_name).suffix}'
            ticket_attachment_upload_file_path = Path(ticket_attachment_directory_path / ticket_attachment_upload_file_uuid_name)
            ticket_attachment_upload_file_path.write_bytes(ticket_attachment_upload_file_content)

            ticket_attachment_object_model = await insert_object_model(
                session=session,
                base_model=TicketAttachments,
                data_model={
                    'ticket_id': ticket_object_model.id,
                    'file_name': ticket_attachment_upload_file_name,
                    'file_uuid_name': ticket_attachment_upload_file_uuid_name,
                    'file_path': ticket_attachment_upload_file_path.as_posix(),
                    'mime_type': ticket_attachment_upload.content_type,
                    'file_size': len(ticket_attachment_upload_file_content),
                },
            )

            logger.debug(
                request.url_for('download_ticket_attachment', ticket_id=str(ticket_attachment_object_model.ticket_id), attachment_id=str(ticket_attachment_object_model.id))
            )

            ticket_attachment_upload.file.close()


    request_type = await select_request_type_description_by_id(session, request_type_id)
    emails = await select_user_emails(session, requester_id)
    subject = f'Ticket #{code}: {request_type}'
    
    
    body_html = build_ticket_email_body(code=code, request_type=request_type, note=note)
    body_text = build_ticket_email_text(code=code, request_type=request_type, note=note)

    #await emit_ticket_event(
    #    session=session,
    #    ticket_id=ticket_object_model.id,
    #    payload={
    #        'type': 'ticket_created',
    #        'requesterId': str(requester_id),
    #        'managerId': str(ticket_object_model.manager_id) if ticket_object_model.manager_id else None,
    #        'groupId': str(group_id) if group_id else None,
    #    },
    #)

    #await send_email(
    #    to=emails,
    #    subject=subject,
    #    body_html=body_html,
    #    body_text=body_text,
    #)

    return response(response_type=1, status_code=HTTP_201_CREATED)




'''

async def emit_ticket_event(
    session: AsyncSession,
    ticket_id: UUID,
    payload: dict,
) -> None:
    """
    Emite el evento a las salas relacionadas con el ticket.
    No bloquea la peticiA3n en caso de error.
    """
    base_payload = {'ticketId': str(ticket_id), **payload}
    rooms = {
        'tickets',  # sala general para que el listado refresque
        f'ticket:{ticket_id}',
    }

    try:
        ticket = await select_ticket_by_id(session=session, ticket_id=ticket_id)

        if ticket and ticket.requester_id:  rooms.add(f'user:{ticket.requester_id}')
        if ticket and ticket.manager_id:    rooms.add(f'user:{ticket.manager_id}')
        if ticket and ticket.group_id:      rooms.add(f'group:{ticket.group_id}')

        for room in rooms:
            await broadcast(room=str(room), payload=base_payload)

    except Exception as exception:
        logger.exception('No se pudo emitir el evento WS del ticket %s: %s', ticket_id, exception)


# id solicitante
@router.get('/select/all/tickets/requester/{requester_id}')
async def get_all_tickets_by_requester_id(request: Request,
                                          session: Annotated[AsyncSession, Depends(database)], 
                                          requester_id: UUID):
    data = await select_all_tickets_by_requester_id(session=session, requester_id=requester_id)

    return response(
        response_type=2,
        status_code=HTTP_200_OK,
        content={'data': data}
    )

# id usuario asignado
#@router.get('/select/all/tickets/assignee/{assignee_id}')
#async def get_all_tickets_by_assignee_id(request: Request,
#                                         session: Annotated[AsyncSession, Depends(database)], 
#                                         assignee_id: UUID):
#    data = await select_all_tickets_by_assignee_id(session=session, assignee_id=assignee_id)
#    return {'data': data}


# encargado
@router.get('/select/all/tickets/manager')
async def get_all_tickets_for_manager(request: Request, session: Annotated[AsyncSession, Depends(database)]):
    data = await select_all_tickets_for_manager(session=session)
    return {'data': data}




@router.get('/select/total/tickets/requester/{requester_id}')
async def get_total_tickets_by_requester_id(request: Request, session: Annotated[AsyncSession, Depends(database)], requester_id: UUID, status: str):
    data = await select_count_tickets_by_requester_id(session=session, requester_id=requester_id, status=status)
    return {'data': data}


@router.get('/select/total/tickets/manager')
async def get_total_tickets_for_manager(request: Request, session: Annotated[AsyncSession, Depends(database)], status: str):
    data = await select_count_tickets_for_manager(session=session, status=status)
    return {'data': data}












@router.get(path='/select/all/types/request')
async def get_all_request_types(request: Request, session: Annotated[AsyncSession, Depends(database)]):
    data = await select_all_request_types(session)
    return {'data': data}

@router.get(path='/select/all/types/priority')
async def get_all_priority_types(request: Request, session: Annotated[AsyncSession, Depends(database)]):
    data = await select_all_priority_types(session)
    return {'data': data}


@router.get(path='/select/all/types/status')
async def get_all_status_types(request: Request, session: Annotated[AsyncSession, Depends(database)]):
    data = await select_all_status_types(session)
    return {'data': data}


@router.get(path='/select/all/users/groups')
async def get_all_user_groups(request: Request, session: Annotated[AsyncSession, Depends(database)]):
    data = await select_all_user_groups(session)
    return {'data': data}


@router.get(path='/select/all/users/support')
async def get_all_support_users(request: Request, session: Annotated[AsyncSession, Depends(database)]):
    data = await select_all_support_users(session)
    return {'data': data}






@router.put(path='/update/ticket/{ticket_id}/status/{status_id}')
async def put_ticket_status(request: Request,
                            session: Annotated[AsyncSession, Depends(database)],
                            ticket_id: UUID,
                            status_id: UUID):
    operation, object_model = await update_ticket(
        session=session,
        context='status',
        ticket_id=ticket_id,
        object_id=status_id)
    
    if operation is None:
        return response(response_type=1, status_code=HTTP_404_NOT_FOUND)
    
    if operation is False:
        return response(response_type=1, status_code=HTTP_422_UNPROCESSABLE_ENTITY)

    status = await select_status_type_description_by_id(session, object_model.status_type_id)

    request_type = await select_request_type_description_by_id(session, object_model.request_type_id)
    
    # debería mandar sólo cuando se toma el ticket o se resuelve??
    if status == 'Resuelto':
        emails = await select_user_emails(session, object_model.requester_id)
        subject = f'Actualización de ticket #{object_model.code}: {request_type}'
        
        body_html = build_ticket_status_email_body(code=object_model.code, status=status)
        body_text = build_ticket_status_email_text(code=object_model.code, status=status)

        await send_email(
            to=emails,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
        )


    await emit_ticket_event(
        session=session,
        ticket_id=ticket_id,
        payload={
            'type': 'ticket_status_updated',
            'statusId': str(status_id),
        },
    )



    return response(
        response_type=1,
        status_code=HTTP_200_OK,
    )

@router.put(path='/update/ticket/{ticket_id}/manager/{manager_id}')
async def put_ticket_manager(request: Request,
                             session: Annotated[AsyncSession, Depends(database)],
                             ticket_id: UUID,
                             manager_id: UUID):
    operation, _ = await update_ticket(
        session=session,
        context='manager',
        ticket_id=ticket_id,
        object_id=manager_id)
    
    if operation is None:
        return response(response_type=1, status_code=HTTP_404_NOT_FOUND)
    
    if operation is False:
        return response(response_type=1, status_code=HTTP_422_UNPROCESSABLE_ENTITY)

    await emit_ticket_event(
        session=session,
        ticket_id=ticket_id,
        payload={
            'type': 'ticket_assigned',
            'managerId': str(manager_id),
        },
    )

    return response(
        response_type=1,
        status_code=HTTP_200_OK,
    )



@router.put(path='/update/ticket/{ticket_id}/read')
async def put_ticket_read_status(request: Request,
                                 session: Annotated[AsyncSession, Depends(database)],
                                 ticket_id: UUID):
    operation, _ = await update_ticket(
        session=session,
        context='read',
        ticket_id=ticket_id)
    
    if operation is None:
        return response(response_type=1, status_code=HTTP_404_NOT_FOUND)
    
    if operation is False:
        return response(response_type=1, status_code=HTTP_422_UNPROCESSABLE_ENTITY)

    await emit_ticket_event(
        session=session,
        ticket_id=ticket_id,
        payload={
            'type': 'ticket_read',
        },
    )

    return response(
        response_type=1,
        status_code=HTTP_200_OK,
    )


@router.put(path='/update/ticket/{ticket_id}/resolved')
async def put_ticket_resolved(request: Request,
                              session: Annotated[AsyncSession, Depends(database)],
                              ticket_id: UUID,
                              is_resolved: bool = Form(...)):
    operation, _ = await update_ticket(
        session=session,
        context='resolved',
        ticket_id=ticket_id,
        is_resolved=is_resolved,
    )

    if operation is None:
        return response(response_type=1, status_code=HTTP_404_NOT_FOUND)
    
    if operation is False:
        return response(response_type=1, status_code=HTTP_422_UNPROCESSABLE_ENTITY)

    await emit_ticket_event(
        session=session,
        ticket_id=ticket_id,
        payload={
            'type': 'ticket_resolved',
            'isResolved': is_resolved,
        },
    )

    return response(
        response_type=1,
        status_code=HTTP_200_OK,
    )


@router.put(path='/update/ticket/{ticket_id}/resolution')
async def put_ticket_resolution(request: Request,
                                session: Annotated[AsyncSession, Depends(database)],
                                ticket_id: UUID,
                                resolution: str = Form(...)):
    operation, _ = await update_ticket(
        session=session,
        context='resolution',
        ticket_id=ticket_id,
        resolution=resolution,
    )

    if operation is None:
        return response(response_type=1, status_code=HTTP_404_NOT_FOUND)
    
    if operation is False:
        return response(response_type=1, status_code=HTTP_422_UNPROCESSABLE_ENTITY)

    await emit_ticket_event(
        session=session,
        ticket_id=ticket_id,
        payload={
            'type': 'ticket_resolution_updated',
        },
    )

    return response(
        response_type=1,
        status_code=HTTP_200_OK,
    )















@router.post(path='/create/ticket', status_code=status.HTTP_201_CREATED)
async def post_ticket(
    request: Request,
    session: Annotated[AsyncSession, Depends(database)],
    code: str = Form(...),
    note: str = Form(''),
    request_type_id: UUID = Form(...),
    priority_type_id: UUID = Form(...),
    status_type_id: UUID = Form(...),
    requester_id: UUID = Form(...),
    group_id: UUID | None = Form(None),
    due_at: str | None = Form(None),
    resolved_at: str | None = Form(None),
    closed_at: str | None = Form(None),
    attachments: (UploadFile | list[UploadFile] | Sequence[UploadFile] | None) = File(None),
):

    ticket_object_model = await insert_ticket(
        session=session,
        schema=TicketRequest(
            code=code,
            note=note,
            request_type_id=request_type_id,
            priority_type_id=priority_type_id,
            status_type_id=status_type_id,
            requester_id=requester_id,
            group_id=group_id,
            due_at=due_at,
            resolved_at=resolved_at,
            closed_at=closed_at,
        )
    )
    if not ticket_object_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No se pudo crear el ticket')
    

    # Normaliza a lista incluso cuando FastAPI entrega un solo UploadFile.
    if attachments is None:
        ticket_attachment_uploads: list[UploadFile] = []
    elif isinstance(attachments, (list, tuple)):
        ticket_attachment_uploads = [uploaded_file for uploaded_file in attachments if uploaded_file is not None]
    else:
        ticket_attachment_uploads = [attachments]
    if len(ticket_attachment_uploads) > 0:
        ticket_attachment_directory_path = Path(TICKETS_ATTACHMENTS_DIRECTORY_PATH / str(ticket_object_model.id))
        ticket_attachment_directory_path.mkdir(parents=True, exist_ok=True)

        for ticket_attachment_upload in ticket_attachment_uploads:
            ticket_attachment_upload: UploadFile

            ticket_attachment_upload_file_name = Path(ticket_attachment_upload.filename).name
            if not ticket_attachment_upload_file_name:
                ticket_attachment_upload.file.close()
                continue

            ticket_attachment_upload_file_content = await ticket_attachment_upload.read()
            ticket_attachment_upload_file_uuid_name = f'{uuid4().hex}{Path(ticket_attachment_upload_file_name).suffix}'
            ticket_attachment_upload_file_path = Path(ticket_attachment_directory_path / ticket_attachment_upload_file_uuid_name)
            ticket_attachment_upload_file_path.write_bytes(ticket_attachment_upload_file_content)

            ticket_attachment_object_model = await insert_object_model(
                session=session,
                base_model=TicketAttachments,
                data_model={
                    'ticket_id': ticket_object_model.id,
                    'file_name': ticket_attachment_upload_file_name,
                    'file_uuid_name': ticket_attachment_upload_file_uuid_name,
                    'file_path': ticket_attachment_upload_file_path.as_posix(),
                    'mime_type': ticket_attachment_upload.content_type,
                    'file_size': len(ticket_attachment_upload_file_content),
                },
            )

            logger.debug(
                request.url_for('download_ticket_attachment', ticket_id=str(ticket_attachment_object_model.ticket_id), attachment_id=str(ticket_attachment_object_model.id))
            )

            ticket_attachment_upload.file.close()


    request_type = await select_request_type_description_by_id(session, request_type_id)
    emails = await select_user_emails(session, requester_id)
    subject = f'Ticket #{code}: {request_type}'
    
    
    body_html = build_ticket_email_body(code=code, request_type=request_type, note=note)
    body_text = build_ticket_email_text(code=code, request_type=request_type, note=note)

    await emit_ticket_event(
        session=session,
        ticket_id=ticket_object_model.id,
        payload={
            'type': 'ticket_created',
            'requesterId': str(requester_id),
            'managerId': str(ticket_object_model.manager_id) if ticket_object_model.manager_id else None,
            'groupId': str(group_id) if group_id else None,
        },
    )

    await send_email(
        to=emails,
        subject=subject,
        body_html=body_html,
        body_text=body_text,
    )

    return response(response_type=1, status_code=HTTP_201_CREATED)



@router.delete(path='/delete/ticket/{ticket_id}')
async def delete_ticket(
    ticket_id: UUID,
    session: Annotated[AsyncGenerator, Depends(database)],
):
    
    ticket_snapshot = await select_ticket_by_id(session=session, ticket_id=ticket_id)
    operation = await delete_ticket_by_ticket_id(session, ticket_id)
    
    if operation is None:
        return response(response_type=1, status_code=HTTP_404_NOT_FOUND)
    
    if operation is False:
        return response(response_type=1, status_code=HTTP_400_BAD_REQUEST)

    await emit_ticket_event(
        session=session,
        ticket_id=ticket_id,
        payload={
            'type': 'ticket_deleted',
            'requesterId': str(ticket_snapshot.requester_id) if ticket_snapshot and ticket_snapshot.requester_id else None,
            'managerId': str(ticket_snapshot.manager_id) if ticket_snapshot and ticket_snapshot.manager_id else None,
            'groupId': str(ticket_snapshot.group_id) if ticket_snapshot and ticket_snapshot.group_id else None,
        },
    )

    return response(
        response_type=1,
        status_code=HTTP_200_OK,
    )


@router.get(
    path='/download/ticket/{ticket_id}/attachments/{attachment_id}',
    name='download_ticket_attachment',
)
async def download_ticket_attachment(
    ticket_id: UUID,
    attachment_id: UUID,
    session: Annotated[AsyncGenerator, Depends(database)],
):
    ticket_attachment_object_model = await select_ticket_attachment_by_id(session=session, attachment_id=attachment_id)
    if not ticket_attachment_object_model or ticket_attachment_object_model.ticket_id != ticket_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Archivo adjunto no encontrado')

    ticket_attachment_upload_file_path = Path(TICKETS_ATTACHMENTS_DIRECTORY_PATH / str(ticket_id) / ticket_attachment_object_model.file_uuid_name)

    if not ticket_attachment_upload_file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Archivo adjunto no disponible')

    return FileResponse(
        path=ticket_attachment_upload_file_path,
        filename=ticket_attachment_object_model.file_name,
        media_type=ticket_attachment_object_model.mime_type or 'application/octet-stream',
    )






@router.post(path='/create/types/request')
async def post_request_type(request: Request,
                         session: Annotated[AsyncSession, Depends(database)],
                         description: str = Form(...),):

    logger.info(msg=f'{request.client.host}:{request.client.port}')

    try:
        object_model = await insert_request_type(session=session, description=description)

        return response(
            response_type=2,
            status_code=HTTP_200_OK,
            media_type='application/json',
            content={'status': True}
        ) if object_model else response(
            response_type=2,
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            media_type='application/json',
            content={'status': 'error'}
        )

    except Exception as exception:
        logger.exception(msg=f'{request.client.host}:{request.client.port}: {exception}')

        return response(
            response_type=2,
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            media_type='application/json',
            content={'message': 'Internal Server Error'}
        )
'''