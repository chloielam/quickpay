from fastapi import APIRouter, HTTPException, status

from .users_schemas import UserBalanceResponse, UserCreate, UserResponse
from .users_services import create_user
from app.users.users_repository import get_user_by_id, list_users
from app.core.errors import ERR_AGE_RESTRICTED, ERR_INVALID_EMAIL

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user_data: UserCreate):
    try:
        return create_user(user_data)
    except ValueError as e:
        msg = str(e)
        if msg in {ERR_AGE_RESTRICTED, ERR_INVALID_EMAIL}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@router.get("/", response_model=list[UserResponse])
def get_users():
    return list_users()


@router.get("/{user_id}/balance", response_model=UserBalanceResponse)
def get_user_balance_endpoint(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserBalanceResponse(uid=user_id, balance=user.balance)