from pydantic import BaseModel 

class UserCreate(BaseModel):
    legal_name: str
    email: str
    age: int

class UserResponse(BaseModel):
    uid: int
    legal_name: str
    email: str
    age: int
    balance: float = 0.0

