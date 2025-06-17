import hashlib

from fastapi import APIRouter
from starlette.requests import Request
from service import product as service

router = APIRouter(prefix="/products", tags=["product"])

@router.post("/{product_id}/like")
def like(request: Request, product_id: int):
    ip = request.client.host
    user_agent = request.headers.get("User-Agent")
    device_id = hashlib.sha256(f"{ip}-{user_agent}".encode()).hexdigest()
    return service.like(product_id, device_id)

@router.get("")
def get_products():
    return service.get_products()

@router.get("/{product_id}")
def get_product(product_id: int):
    return service.get_product(product_id)
