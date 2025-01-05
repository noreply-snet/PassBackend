from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

# Pydantic Schema for Create
class NoteDataCreate(BaseModel):
    title: str = Field(..., example="Example Title")
    tags: List[str] = Field(..., example=["tag1", "tag2"])
    massage: str = Field(..., example="This is a note message.")
    color: str = Field(..., example="#FF5733")  # Example hex color code

# Pydantic Schema for Update
class NoteDataUpdate(NoteDataCreate):
    id: int

# Pydantic Schema for Read
class NoteDataRead(NoteDataUpdate):
    created_at: datetime = Field(..., example="2023-01-05T12:34:56Z")

    class Config:
        orm_mode = True
