from pydantic import BaseModel

class DepositCreate(BaseModel):
    amount: float
    user_id: str

class DepositResponse(BaseModel):
    tid: int
    amount: float
    user_id: str
    timestamp: str

class TransferCreate(BaseModel):
    amount: float
    sender_id: str
    receiver_id: str

class TransferResponse(BaseModel):
    tid: int
    amount: float
    sender_id: str
    receiver_id: str
    timestamp: str
