from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from cruds.pass_crud import create_password, read_password, update_password, delete_password
from schemas.pass_schemas import PassDataCreate, PassDataUpdate, PassDataRead

router = APIRouter()

@router.post("/", response_model=PassDataRead)
def create_password_route(password: PassDataCreate, db: Session = Depends(get_db)):
    return create_password(db, password)

@router.get("/{password_id}", response_model=PassDataRead)
def read_password_route(password_id: int, db: Session = Depends(get_db)):
    return read_password(db, password_id)

@router.put("/{password_id}", response_model=PassDataRead)
def update_password_route(password_id: int, password: PassDataUpdate, db: Session = Depends(get_db)):
    return update_password(db, password_id, password)

@router.delete("/{password_id}", response_model=PassDataRead)
def delete_password_route(password_id: int, db: Session = Depends(get_db)):
    return delete_password(db, password_id)
