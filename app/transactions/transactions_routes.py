from fastapi import APIRouter

from .transactions_services import create_deposit, create_transfer
from .transactions_schemas import DepositCreate, DepositResponse, TransferCreate, TransferResponse

router = APIRouter(prefix="/transactions")

@router.post("/deposit")
def create_new_deposit(deposit_data: DepositCreate):
    try:
        return create_deposit(deposit_data)
    except ValueError as e:
        return {"error": str(e)}
    
@router.post("/transfer")
def create_new_transfer(transfer_data: TransferCreate, sender_balance: float) -> TransferResponse:
    try:
        return create_transfer(transfer_data, sender_balance)
    except ValueError as e:
        return {"error": str(e)}