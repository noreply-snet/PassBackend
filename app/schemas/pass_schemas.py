from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Pydantic Schema for Create
class PassDataCreate(BaseModel):
    acc_name: str = Field(..., example="Example Account")
    url: Optional[str] = Field(None, example="https://example.com")
    loginid: str = Field(..., example="exampleuser")
    password: str = Field(..., example="password123")
    ass_email: Optional[str] = Field(None, example="example@example.com")
    notes: Optional[str] = Field(None, example="These are some additional notes.")

# Pydantic Schema for Update
class PassDataUpdate(PassDataCreate):
    id: int

# Pydantic Schema for Read
class PassDataRead(PassDataUpdate):
    created_at: datetime = Field(..., example="2023-01-05T12:34:56Z")

    class Config:
        orm_mode = True
