from datetime import datetime
from typing import List

from pydantic import BaseModel


class ProductResponse(BaseModel):
    product_id: int
    user_id: int
    title: str
    description: str
    image_url: str
    created_at: datetime

class ProductDetailedResponse(BaseModel):
    product_id: int
    user_id: int
    title: str
    description: str
    images: List[str]
    like_count: int
    created_at: datetime


class ProductRequest(BaseModel):
    title: str
    description: str = ""