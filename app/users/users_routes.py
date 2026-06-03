from fastapi import APIRouter, HTTPException, status

from .users_schemas import UserCreate, UserResponse
from .users_services import create_user
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