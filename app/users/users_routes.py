from fastapi import APIRouter

from .users_schemas import UserCreate, UserResponse
from .users_services import create_user

router = APIRouter(prefix="/users")

@router.post("/create")
def create_new_user(user_data: UserCreate):
    try:
        return create_user(user_data)
    except ValueError as e:
        return {"error": str(e)}