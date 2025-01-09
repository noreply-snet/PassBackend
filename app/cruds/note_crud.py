from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from ..models.main_models import NoteDataModel
from ..schemas.note_schemas import NoteDataCreate, NoteDataUpdate

def create_note(db: Session, note: NoteDataCreate):
    db_note = NoteDataModel(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def read_all_notes(db: Session):
    db_note = db.query(NoteDataModel).all()
    if not db_note:
        raise HTTPException(status_code=404, detail="Notes data not found")
    return db_note

def read_note(db: Session, note_id: int):
    db_note = db.query(NoteDataModel).filter(NoteDataModel.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note data not found")
    return db_note

def update_note(db: Session, note: NoteDataUpdate):
    db_note = db.query(NoteDataModel).filter(NoteDataModel.id == note.id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note data not found")
    for key, value in note.model_dump(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int):
    db_note = db.query(NoteDataModel).filter(NoteDataModel.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note data not found")
    db.delete(db_note)
    db.commit()
    return JSONResponse(
        content={"msg": f"Note data with ID {note_id} has been deleted successfully."},
        status_code=status.HTTP_200_OK,
    )
