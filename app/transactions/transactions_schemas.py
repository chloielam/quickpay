from pydantic import BaseModel

class DepositCreate(BaseModel):
    amount: float
    user_id: int

class DepositResponse(BaseModel):
    tid: int
    amount: float
    user_id: int
    timestamp: str

class TransferCreate(BaseModel):
    amount: float
    sender_id: int
    receiver_id: int

class TransferResponse(BaseModel):
    tid: int
    amount: float
    sender_id: int
    receiver_id: int
    timestamp: str
