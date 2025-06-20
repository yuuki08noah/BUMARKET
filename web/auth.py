import time

import bcrypt
import jwt
from fastapi import APIRouter, Body
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from service import user as service

from data import user as data

from model.user import UserAuthentication

router = APIRouter(prefix="", tags=["auth"])
private_key = b"key"

@router.post("/login")
def login(response: Response, user_authentication: UserAuthentication = Body(...)):
    username = user_authentication.username

    if bcrypt.checkpw(user_authentication.password.encode(), data.get_password(username).encode()):
        now = int(time.time())
        exp = now + 86400
        payload = {
            "username": username,
            "user_id":data.get_user_id_by_username(username),
            "iat": now,
            "exp": exp,
            "admin": bool(data.is_admin(username))
        }
        encoded_jwt = jwt.encode(payload, private_key, algorithm="HS256")

        response.set_cookie(key="token", value=encoded_jwt)
        response.status_code = status.HTTP_200_OK
        response.body = b'successfully logged in'
        return response
    return response

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="token")
    response.status_code = status.HTTP_200_OK
    response.body = b'successfully logged out'
    return response

@router.get("/me")
def me(request: Request):
    sent = request.cookies.get("token")
    if not sent:
        return JSONResponse({"error": "jwt required"}, status_code=401)
    decoded = jwt.decode(sent, private_key, algorithms=["HS256"])
    user_id = decoded.get("user_id")

    return service.get_user(user_id)