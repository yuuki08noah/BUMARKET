import json
from typing import List

import jwt
from fastapi import APIRouter, Body, UploadFile, File, Form
from starlette.requests import Request
from starlette.responses import JSONResponse

from exception.user import UserNotExistException
from service import product as service

from model.product import ProductRequest
from service.product import get_product
from util import get_user_id
from web.auth import private_key

router = APIRouter(prefix="/seller/products", tags=["product"])

@router.post("")
def create(request: Request, product: str = Form(...), img: List[UploadFile] = File(...)):
    user_id = get_user_id(request)

    try:
        product_dict = json.loads(product)
        product_model = ProductRequest(**product_dict)
    except Exception as e:
        return JSONResponse({"error": "Invalid product format", "details": str(e)}, status_code=400)

    service.create_product(user_id, product_model, img)

@router.patch("/{product_id}")
def create(request: Request, product_id: int, product: str = Form(...), img: List[UploadFile] = File(...)):
    user_id = get_user_id(request)
    try:
        product_dict = json.loads(product)
        product_model = ProductRequest(**product_dict)
    except Exception as e:
        return JSONResponse({"error": "Invalid product format", "details": str(e)}, status_code=400)

    service.update_product(product_id, user_id, product_model, img)

@router.get("/my")
def my_products(request: Request):
    user_id = get_user_id(request)
    return service.get_products_by_user_id(user_id)

@router.delete("/{product_id}")
def delete(request: Request, product_id: int):
    user_id = get_user_id(request)
    if get_product(user_id).user_id != user_id:
        raise UserNotExistException(user_id)
    return service.delete_by_product_id(product_id)

