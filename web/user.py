import jwt
from fastapi import APIRouter, Body
from starlette.requests import Request
from starlette.responses import JSONResponse

from model.user import UserCreation
from service import user as service
from service.user import row_to_model

from web.auth import private_key

router = APIRouter(prefix="/admin/sellers", tags=["product"])


@router.post("")
def create(request: Request, user: UserCreation = Body(...)):
    sent = request.cookies.get("token")
    if not sent:
        return JSONResponse({"error": "jwt required"}, status_code=401)
    decoded = jwt.decode(sent, private_key, algorithms=["HS256"])
    is_admin = decoded.get("admin")
    if not is_admin:
        return JSONResponse({"error": "admin required"}, status_code=401)

    service.create_user(user)


@router.get("")
def users(request: Request):
    sent = request.cookies.get("token")
    print(sent)
    if not sent:
        return JSONResponse({"error": "jwt required"}, status_code=401)
    decoded = jwt.decode(sent, private_key, algorithms=["HS256"])
    is_admin = decoded.get("admin")
    if not is_admin:
        return JSONResponse({"error": "admin required"}, status_code=401)

    return service.get_users()

