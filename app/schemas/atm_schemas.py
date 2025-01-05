
from pydantic import BaseModel, Field
from datetime import datetime

# Pydantic Schema for Create
class AtmDataCreate(BaseModel):
    card_number: int = Field(..., example=1234567890123456)
    name: str = Field(..., example="John Doe")
    exp_date: str = Field(..., pattern=r"^(0[1-9]|1[0-2])\/\d{2}$", example="12/25")  # MM/YY format
    cvv: int = Field(..., ge=100, le=999, example=123)  # CVV is usually 3 digits


# Pydantic Schema for Update
class AtmDataUpdate(AtmDataCreate):
    id: int


# Pydantic Schema for Read
class AtmDataRead(AtmDataUpdate):
    created_at: datetime = Field(..., example="2023-01-05T12:34:56Z")

    class Config:
        orm_mode = True

