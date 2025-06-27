import jwt
from fastapi import APIRouter, Body
from starlette.requests import Request
from starlette.responses import JSONResponse

from exception.auth import AdminRequiredException
from model.user import UserCreation
from service import user as service
from util import get_admin

router = APIRouter(prefix="/admin/sellers", tags=["product"])

@router.post("")
def create(request: Request, user: UserCreation = Body(...)):
    is_admin = get_admin(request)
    if not is_admin: raise AdminRequiredException()
    service.create_user(user)

@router.get("")
def users(request: Request):
    is_admin = get_admin(request)
    if not is_admin: raise AdminRequiredException()
    return service.get_users()

