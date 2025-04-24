from fastapi import APIRouter
from starlette.responses import JSONResponse

clients_router = APIRouter()

@clients_router.get('/client/{idx}')
def get_client(idx: int) -> JSONResponse:
    ...