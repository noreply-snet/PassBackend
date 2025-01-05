from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from cruds.bank_crud import create_bank, read_bank, update_bank, delete_bank
from schemas.bank_schemas import BankDataCreate, BankDataUpdate, BankDataRead

router = APIRouter()

@router.post("/", response_model=BankDataRead)
def create_bank_route(bank: BankDataCreate, db: Session = Depends(get_db)):
    return create_bank(db, bank)

@router.get("/{bank_id}", response_model=BankDataRead)
def read_bank_route(bank_id: int, db: Session = Depends(get_db)):
    return read_bank(db, bank_id)

@router.put("/{bank_id}", response_model=BankDataRead)
def update_bank_route(bank_id: int, bank: BankDataUpdate, db: Session = Depends(get_db)):
    return update_bank(db, bank_id, bank)

@router.delete("/{bank_id}", response_model=BankDataRead)
def delete_bank_route(bank_id: int, db: Session = Depends(get_db)):
    return delete_bank(db, bank_id)
