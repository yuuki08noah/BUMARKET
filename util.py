import hashlib

import jwt
from starlette.requests import Request
from starlette.responses import JSONResponse

from exception.auth import JwtRequiredException

private_key = b"key"

def get_username(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise JwtRequiredException()
    decoded = jwt.decode(token, private_key, algorithms=["HS256"])
    username = decoded.get("username")
    return username

def get_admin(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise JwtRequiredException()
    decoded = jwt.decode(token, private_key, algorithms=["HS256"])
    admin = decoded.get("admin")
    return admin

def get_user_id(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise JwtRequiredException()
    decoded = jwt.decode(token, private_key, algorithms=["HS256"])
    user_id = decoded.get("user_id")
    return user_id

def get_device_id(request: Request):
    ip = request.client.host
    user_agent = request.headers.get("User-Agent")
    device_id = hashlib.sha256(f"{ip}-{user_agent}".encode()).hexdigest()
    return device_id