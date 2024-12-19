from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class CourierBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    
    
class CourierCreate(CourierBase):
    password: str
    
    
class CourierOut(CourierBase):
    uuid: UUID
    is_active: bool
    
    class Config:
        from_attributes = True
        

# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
    uuid: UUID | None = None