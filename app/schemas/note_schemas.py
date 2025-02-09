from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

# Pydantic Schema for Create
class NoteDataCreate(BaseModel):
    title: str = Field(..., example="Example Title")
    tags: List[str] = Field(..., example=["tag1", "tag2"])
    message: str = Field(..., example="This is a note message.")
    color: str = Field(..., example="red")  # Example hex color code

# Pydantic Schema for Update
class NoteData(NoteDataCreate):
    id: int

# Pydantic Schema for Read
class NoteDataRead(NoteData):
    created_at: datetime = Field(..., example="2023-01-05T12:34:56Z")
    
    class Config:
        from_attributes = True

# Pydantic Schema for Read Full Note Data
class NoteDataFull(NoteData):
    updated_at: datetime = Field(..., example="2023-01-05T12:34:56Z")

    class Config:
        from_attributes = True
