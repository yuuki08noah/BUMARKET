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

def update_product(product_id, user_id, product: ProductRequest, url):
    query = f"update products set user_id=%s, title=%s, description=%s, image_url=%s where product_id=%s"
    cur.execute(query, (user_id, product.title, product.description, url[0], product_id))
    delete_images(product_id)
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

def delete_images(product_id):
    print(product_id)
    query = 'delete from product_images where product_id=%s'
    cur.execute(query, (product_id,))
    con.commit()


def get_product_by_product_id_and_user_id(product_id, user_id):
    query = f'select * from products where product_id={product_id} AND user_id={user_id}'
    cur.execute(query)
    return cur.fetchone()

def get_urls_by_product_id(product_id):
    query = f'select image_url from product_images where product_id={product_id}'
    cur.execute(query)
    return cur.fetchall()

def delete_product(product_id):
    query = f'delete from products where product_id={product_id}'
    cur.execute(query)
    con.commit()
