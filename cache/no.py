from cache import redis_client

def toggle_like(product_id, device_id):
    product_key = f"like:{product_id}"
    user_key = f"like:{device_id}"

    if redis_client.sismember(product_key, user_key):
        redis_client.srem(product_key, device_id)
        redis_client.srem(user_key, product_key)
        redis_client.zincrby("like_ranking", -1, product_id)
    else:
        redis_client.sadd(product_key, device_id)
        redis_client.sadd(user_key, product_key)
        redis_client.zincrby("like_ranking", 1, product_id)

def get(product_id):
    product_key = f"like:{product_id}"
    return redis_client.scard(product_key)