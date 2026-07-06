from pydantic import BaseModel 

class UserCreate(BaseModel):
    user_id: str
    legal_name: str
    email: str
    age: int

class UserResponse(BaseModel):
    uid: str
    legal_name: str
    email: str
    age: int
    balance: float = 0.0

class UserBalanceResponse(BaseModel):
    uid: str
    balance: float
