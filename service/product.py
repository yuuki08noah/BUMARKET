import os
import shutil

from cache import no as redis
from data import product as data
from exception.product import ImageInvalidException
from model.product import ProductResponse, ProductRequest, ProductDetailedResponse

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
    product = data.get_product(product_id)
    images = data.get_urls_by_product_id(product_id)
    like_count = data.get_like_count(product_id)
    product_id, user_id, title, description, image_url, created_at = product
    return ProductDetailedResponse(
        product_id=product_id,
        user_id=user_id,
        title=title,
        description=description,
        created_at=created_at,
        images=list(map(lambda x: x[0], images)),
        like_count=like_count
    )

def create_product(user_id: int, product: ProductRequest, imgs):
    paths = create_images(imgs)
    data.create_product(user_id, product, paths)

def get_products_by_user_id(user_id):
    return list(map(row_to_model, data.get_products_by_user_id(user_id)))

def update_product(product_id, user_id, product, imgs):
    urls = data.get_urls_by_product_id(product_id)
    if urls:
        delete_images(urls)

    paths = create_images(imgs)
    data.update_product(product_id, user_id, product, paths)

def create_images(imgs):
    paths = []
    for img in imgs:
        global inc
        if not img.content_type.startswith('image/'):
            raise ImageInvalidException()
        name, ext = os.path.splitext(img.filename)
        save_filename = f'{name}_{inc}{ext}'
        inc += 1
        UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")  # 현재 프로젝트 내부의 uploads 폴더

        file_path = os.path.join(UPLOAD_DIR, save_filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(img.file, f)
        paths.append(file_path)
    return paths

def delete_images(paths):
    for path in paths:
        if os.path.isfile(path[0]):
            os.remove(path[0])

def delete_by_product_id(product_id):
    urls = data.get_urls_by_product_id(product_id)
    if urls:
        delete_images(urls)
    data.delete_product(product_id)
    data.delete_images(product_id)
    return True