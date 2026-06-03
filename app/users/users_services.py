from .users_schemas import UserCreate, UserResponse
from .users_validators import validate_age, validate_email
from app.users.users_repository import get_user_by_email, save_user


def create_user(user_data: UserCreate) -> UserResponse:
    validate_age(user_data.age)
    validate_email(user_data.email)

    return save_user(user_data)

