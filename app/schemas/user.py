from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UpdatePassword(BaseModel):
    password: str

class AdminUserCreate(UserCreate):
    role: str

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True