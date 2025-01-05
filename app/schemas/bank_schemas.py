from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Pydantic Schema for Create
class BankDataCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    bank_name: str = Field(..., example="Example Bank")
    branch_name: str = Field(..., example="Example Branch")
    acc_type: str = Field(..., example="Savings")
    acc_number: str = Field(..., example="1234567890")
    ifsc_code: str = Field(..., example="IFSC0000123")
    mirc_code: Optional[str] = Field(None, example="MICR0000123")
    note: Optional[str] = Field(None, example="Some additional notes.")
    rmn: str = Field(..., example="9876543210")

# Pydantic Schema for Update
class BankDataUpdate(BankDataCreate):
    id: int

# Pydantic Schema for Read
class BankDataRead(BankDataUpdate):
    created_at: datetime = Field(..., example="2023-01-05T12:34:56Z")

    class Config:
        orm_mode = True
