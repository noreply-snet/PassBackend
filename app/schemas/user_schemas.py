from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserUpdatePassword(BaseModel):
    u_id: UUID
    password: str

class UserUpdateEmail(BaseModel):
    u_id: UUID
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserUpdateEmail):
    updated_at: datetime

    class Config:
        orm_mode = True

class UserFull(UserResponse):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
