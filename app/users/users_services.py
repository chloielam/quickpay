from .users_schemas import UserCreate, UserResponse
from .users_validators import validate_age, validate_email  

def create_user(user_data: UserCreate) -> UserResponse:
    validate_age(user_data.age)
    validate_email(user_data.email)
    return UserResponse(uid=1, legal_name=user_data.legal_name, email=user_data.email, age=user_data.age)

