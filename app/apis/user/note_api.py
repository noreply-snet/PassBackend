from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import security
from ...database.session import get_db
from ...cruds.note_crud import create_note, read_note, update_note, delete_note, read_all_notes
from ...schemas.note_schemas import NoteDataCreate, NoteData
from typing import List

router = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)


@router.post("/", response_model=NoteData)
def create_note_route(note: NoteDataCreate, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return create_note(db, user_id, note) 

@router.get("/all", response_model=List[NoteData])
def read_all_notes_route(db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return read_all_notes(db, user_id)

@router.get("/{note_id}", response_model=NoteData)
def read_note_route(note_id: int, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return read_note(db, user_id, note_id)

@router.put("/", response_model=NoteData)
def update_note_route(note: NoteData, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return update_note(db, user_id, note)

@router.delete("/{note_id}")
def delete_note_route(note_id: int, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return delete_note(db, user_id, note_id)
