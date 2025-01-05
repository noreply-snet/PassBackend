from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from cruds.note_crud import create_note, read_note, update_note, delete_note
from schemas.note_schemas import NoteDataCreate, NoteDataUpdate, NoteDataRead

router = APIRouter()

@router.post("/", response_model=NoteDataRead)
def create_note_route(note: NoteDataCreate, db: Session = Depends(get_db)):
    return create_note(db, note)

@router.get("/{note_id}", response_model=NoteDataRead)
def read_note_route(note_id: int, db: Session = Depends(get_db)):
    return read_note(db, note_id)

@router.put("/{note_id}", response_model=NoteDataRead)
def update_note_route(note_id: int, note: NoteDataUpdate, db: Session = Depends(get_db)):
    return update_note(db, note_id, note)

@router.delete("/{note_id}", response_model=NoteDataRead)
def delete_note_route(note_id: int, db: Session = Depends(get_db)):
    return delete_note(db, note_id)
