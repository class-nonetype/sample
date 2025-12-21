from src.utils.properties import API_PREFIX
from src.api.routers.versions.v1 import (
    authentication,
    #application,
    admin,
    web_socket,
)


from fastapi import APIRouter


API_ROUTERS = {
    'admin' : [admin],
    #'application' : [application],
    'authentication': [authentication],
    'web_socket': [web_socket],
}


router = APIRouter()

for key, values in API_ROUTERS.items():
    for value in values:
        router.include_router(router=value, prefix=API_PREFIX[key])
