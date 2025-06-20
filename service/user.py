from cache import no as redis
from data import user as data
from model.user import UserResponse, UserCreation


def like(product_id: int, device_id: str):
    redis.toggle_like(product_id, device_id)
    score = redis.get(product_id)
    return {
        "product_id": product_id,
        "count": score
    }

def row_to_model(user) -> UserResponse:
    user_id, username, password, name, admin, created_at = user
    return UserResponse(
        user_id=user_id,
        username=username,
        name=name,
        is_admin=admin,
        created_at=created_at
    )

def get_users():
    return list(map(row_to_model, data.get_users()))

def get_user(user_id):
    return row_to_model(data.get_user(user_id))

def create_user(user: UserCreation):
    data.create_user(user)