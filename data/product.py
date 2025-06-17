from model.product import ProductRequest
from . import con, cur

def get_products():
    query = 'select * from products'
    cur.execute(query)
    return cur.fetchall()


def get_product(product_id):
    query = f'select * from products where product_id={product_id}'
    cur.execute(query)
    return cur.fetchone()

def create_product(user_id, product: ProductRequest, url):
    query = f"insert into products(user_id, title, description, image_url) values(%s, %s, %s, %s)"
    cur.execute(query, (user_id, product.title, product.description, url[0]))
    product_id = cur.lastrowid
    for i in url:
        create_image(product_id, i)
    con.commit()


def get_products_by_user_id(user_id):
    query = f'select * from products where user_id=%s'
    cur.execute(query, (user_id, ))
    return cur.fetchall()

def create_image(product_id, image_url):
    query = f'insert into product_images(product_id, image_url) values(%s, %s)'
    cur.execute(query, (product_id, image_url))
    con.commit()