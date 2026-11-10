from pydantic import BaseModel, Field
from decimal import Decimal 

class UserAuth(BaseModel):
    username: str  = Field(min_length=3, max_length=50)
    password: str 
    
class UserOut(BaseModel):
    id: int
    username: str 
    balance: Decimal
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TransferIn(BaseModel):
    receiver_username: str
    amount: Decimal = Field(gt=Decimal("0"))