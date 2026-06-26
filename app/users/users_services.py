from .users_schemas import UserBalanceResponse, UserCreate, UserResponse
from .users_validators import validate_age, validate_email
from app.core.errors import ERR_DUPLICATE_USER_ID, ERR_USER_NOT_FOUND
from app.users.users_repository import get_user_by_id, list_users, save_user


def create_user(user_data: UserCreate) -> UserResponse:
    validate_age(user_data.age)
    validate_email(user_data.email)
    if get_user_by_id(user_data.user_id):
        raise ValueError(ERR_DUPLICATE_USER_ID)

    return save_user(user_data)


def get_all_users() -> list[UserResponse]:
    return list_users()


def get_user_balance_info(user_id: int) -> UserBalanceResponse:
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError(ERR_USER_NOT_FOUND)
    return UserBalanceResponse(uid=user_id, balance=user.balance)
