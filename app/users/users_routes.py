from fastapi import APIRouter, HTTPException, status

from .users_schemas import UserBalanceResponse, UserCreate, UserResponse
from .users_services import create_user, get_all_users, get_user_balance_info
from app.core.errors import ERR_AGE_RESTRICTED, ERR_DUPLICATE_USER_ID, ERR_INVALID_EMAIL, ERR_USER_NOT_FOUND

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user_data: UserCreate):
    try:
        return create_user(user_data)
    except ValueError as e:
        msg = str(e)
        if msg in {ERR_AGE_RESTRICTED, ERR_INVALID_EMAIL, ERR_DUPLICATE_USER_ID}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@router.get("/", response_model=list[UserResponse])
def get_users():
    return get_all_users()


@router.get("/{user_id}/balance", response_model=UserBalanceResponse)
def get_user_balance_endpoint(user_id: int):
    try:
        return get_user_balance_info(user_id)
    except ValueError as e:
        if str(e) == ERR_USER_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
