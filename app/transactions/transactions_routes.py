from fastapi import APIRouter, HTTPException, status

from .transactions_services import create_deposit, create_transfer
from .transactions_schemas import DepositCreate, DepositResponse, TransferCreate, TransferResponse
from app.transactions.transactions_repository import list_deposits, list_transfers
from app.core.errors import (
    ERR_DEPOSIT_LIMIT,
    ERR_INSUFFICIENT_FUNDS,
    ERR_INVALID_TRANSFER_AMOUNT,
    ERR_USER_NOT_FOUND,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/deposit", response_model=DepositResponse, status_code=status.HTTP_201_CREATED)
def create_new_deposit(deposit_data: DepositCreate):
    try:
        return create_deposit(deposit_data)
    except ValueError as e:
        msg = str(e)
        if msg == ERR_DEPOSIT_LIMIT:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        if msg == ERR_USER_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@router.post("/transfer", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_new_transfer(transfer_data: TransferCreate) -> TransferResponse:
    try:
        return create_transfer(transfer_data)
    except ValueError as e:
        msg = str(e)
        if msg == ERR_INSUFFICIENT_FUNDS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        if msg == ERR_INVALID_TRANSFER_AMOUNT:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        if msg == ERR_USER_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@router.get("/deposits", response_model=list[DepositResponse])
def get_deposits():
    return list_deposits()


@router.get("/transfers", response_model=list[TransferResponse])
def get_transfers():
    return list_transfers()
