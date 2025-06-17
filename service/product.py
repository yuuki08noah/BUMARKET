import os
import shutil

from starlette.responses import JSONResponse

from cache import no as redis
from data import product as data
from model.product import ProductResponse, ProductRequest
inc = 0

def like(product_id: int, device_id: str):
    redis.toggle_like(product_id, device_id)
    score = redis.get(product_id)
    return {
        "product_id": product_id,
        "count": score
    }

def row_to_model(product) -> ProductResponse:
    product_id, user_id, title, description, image_url, created_at = product
    return ProductResponse(
        product_id=product_id,
        user_id=user_id,
        title=title,
        description=description,
        image_url=image_url,
        created_at=created_at
    )

def get_products():
    return list(map(row_to_model, data.get_products()))


def get_product(product_id):
    return row_to_model(data.get_product(product_id))

def create_product(user_id: int, product: ProductRequest, imgs):
    paths = []
    for img in imgs:
        global inc
        if not img.content_type.startswith('image/'):
            return JSONResponse({"error": "Invalid image type"}, status_code=404)
        name, ext = os.path.splitext(img.filename)
        save_filename = f'{name}_{inc}{ext}'
        inc += 1
        UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")  # 현재 프로젝트 내부의 uploads 폴더

        file_path = os.path.join(UPLOAD_DIR, save_filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(img.file, f)
        paths.append(file_path)

    data.create_product(user_id, product, paths)


def get_products_by_user_id(user_id):
    return data.get_products_by_user_id(user_id)