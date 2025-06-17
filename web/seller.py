import json
import os
import shutil
from typing import List

import jwt
from fastapi import APIRouter, Body, UploadFile, File, Form
from starlette.requests import Request
from starlette.responses import JSONResponse

from service import product as service

from model.product import ProductRequest
from web.auth import private_key

router = APIRouter(prefix="/seller/products", tags=["product"])

@router.post("")
def create(request: Request, product: str = Form(...), img: List[UploadFile] = File(...)):

    sent = request.cookies.get("token")
    if not sent:
        return JSONResponse({"error": "jwt required"}, status_code=401)
    decoded = jwt.decode(sent, private_key, algorithms=["HS256"])
    user_id = decoded.get("user_id")

    try:
        product_dict = json.loads(product)
        product_model = ProductRequest(**product_dict)
    except Exception as e:
        return JSONResponse({"error": "Invalid product format", "details": str(e)}, status_code=400)


    service.create_product(user_id, product_model, img)

@router.get("/my")
def my_products(request: Request):
    sent = request.cookies.get("token")
    if not sent:
        return JSONResponse({"error": "jwt required"}, status_code=401)
    decoded = jwt.decode(sent, private_key, algorithms=["HS256"])
    user_id = decoded.get("user_id")

    return service.get_products_by_user_id(user_id)

