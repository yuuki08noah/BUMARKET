import time

import bcrypt
import jwt
from fastapi import APIRouter, Body
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

import util
from service import user as service
from util import private_key

from data import user as data

from model.user import UserAuthentication

router = APIRouter(prefix="", tags=["auth"])

def create_token(username, user_id, admin):
    now = int(time.time())
    exp = now + 86400
    payload = {
        "username": username,
        "user_id": user_id,
        "iat": now,
        "exp": exp,
        "admin": admin
    }
    encoded_jwt = jwt.encode(payload, private_key, algorithm="HS256")

    return encoded_jwt

@router.post("/login")
def login(response: Response, user_authentication: UserAuthentication = Body(...)):
    username = user_authentication.username
    if bcrypt.checkpw(user_authentication.password.encode(), data.get_password(username).encode()):
        token = create_token(username, data.get_user_id_by_username(username), bool(data.is_admin(username)))
        response.set_cookie(key="token", value=token)
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
    user_id = util.get_user_id(request)
    return service.get_user(user_id)