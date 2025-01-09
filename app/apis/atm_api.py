from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..cruds.atm_crud import create_atm, read_atm, update_atm, delete_atm, read_all_atms
from ..schemas.atm_schemas import AtmDataCreate, AtmData
from typing import List

router = APIRouter()

@router.post("/", response_model=AtmData)
def create_atm_route(atm: AtmDataCreate, db: Session = Depends(get_db)):
    return create_atm(db, atm)

@router.get("/all", response_model=List[AtmData])
def read_atm_route( db: Session = Depends(get_db)):
    return read_all_atms(db)

@router.get("/{atm_id}", response_model=AtmData)
def read_atm_route(atm_id: int, db: Session = Depends(get_db)):
    return read_atm(db, atm_id)

@router.put("/", response_model=AtmData)
def update_atm_route(atm: AtmData, db: Session = Depends(get_db)):
    return update_atm(db, atm)

@router.delete("/{atm_id}")
def delete_atm_route(atm_id: int, db: Session = Depends(get_db)):
    return delete_atm(db, atm_id)
