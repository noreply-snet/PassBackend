from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from cruds.atm_crud import create_atm, read_atm, update_atm, delete_atm
from schemas.atm_schemas import AtmDataCreate, AtmDataUpdate, AtmDataRead

router = APIRouter()

@router.post("/", response_model=AtmDataRead)
def create_atm_route(atm: AtmDataCreate, db: Session = Depends(get_db)):
    return create_atm(db, atm)

@router.get("/{atm_id}", response_model=AtmDataRead)
def read_atm_route(atm_id: int, db: Session = Depends(get_db)):
    return read_atm(db, atm_id)

@router.put("/{atm_id}", response_model=AtmDataRead)
def update_atm_route(atm_id: int, atm: AtmDataUpdate, db: Session = Depends(get_db)):
    return update_atm(db, atm_id, atm)

@router.delete("/{atm_id}", response_model=AtmDataRead)
def delete_atm_route(atm_id: int, db: Session = Depends(get_db)):
    return delete_atm(db, atm_id)
