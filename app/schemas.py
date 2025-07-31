from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

# New Pydantic models for UserCustom

class UserCustomBase(BaseModel):
    u_name: str
    email: str
    gender: Optional[str] = None
    mobile_no: Optional[str] = None
    role_id: Optional[int] = None

class UserCustomCreate(UserCustomBase):
    u_password: bytes

class UserCustomUpdate(BaseModel):
    u_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    mobile_no: Optional[str] = None
    role_id: Optional[int] = None


class UserCustom(UserCustomBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
