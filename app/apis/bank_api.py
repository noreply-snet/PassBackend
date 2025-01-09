from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..cruds.bank_crud import create_bank, read_bank, update_bank, delete_bank, read_all_banks
from ..schemas.bank_schemas import BankDataCreate, BankData
from typing import List

router = APIRouter()

@router.post("/", response_model=BankData)
def create_bank_route(bank: BankDataCreate, db: Session = Depends(get_db)):
    return create_bank(db, bank)

@router.get("/all", response_model=List[BankData])
def read_all_banks_route(db: Session = Depends(get_db)):
    return read_all_banks(db)

@router.get("/{bank_id}", response_model=BankData)
def read_bank_route(bank_id: int, db: Session = Depends(get_db)):
    return read_bank(db, bank_id)

@router.put("/", response_model=BankData)
def update_bank_route(bank: BankData, db: Session = Depends(get_db)):
    return update_bank(db, bank)

@router.delete("/{bank_id}")
def delete_bank_route(bank_id: int, db: Session = Depends(get_db)):
    return delete_bank(db, bank_id)
