from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import security
from ...database.session import get_db
from ...cruds.bank_crud import create_bank, read_bank, update_bank, delete_bank, read_all_banks
from ...schemas.bank_schemas import BankDataCreate, BankData
from typing import List

router = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)

@router.post("/", response_model=BankData)
def create_bank_route(bank: BankDataCreate, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return create_bank(db, user_id, bank)

@router.get("/all", response_model=List[BankData])
def read_all_banks_route(db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return read_all_banks(db, user_id)

@router.get("/{bank_id}", response_model=BankData)
def read_bank_route(bank_id: int, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return read_bank(db, user_id, bank_id)

@router.put("/", response_model=BankData)
def update_bank_route(bank: BankData, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return update_bank(db, user_id, bank)

@router.delete("/{bank_id}")
def delete_bank_route(bank_id: int, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return delete_bank(db, user_id, bank_id)
