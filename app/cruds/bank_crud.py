from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from ..models.main_models import BankDataModel
from ..schemas.bank_schemas import BankDataCreate, BankData

def create_bank(db: Session, user_id: str, bank: BankDataCreate):
    db_bank = BankDataModel(**bank.model_dump(), user_u_id=user_id)
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

def read_all_banks(db: Session, user_id: str):
    db_banks = db.query(BankDataModel).filter(BankDataModel.user_u_id == user_id).all()
    if not db_banks:
        raise HTTPException(status_code=404, detail="Banks data not found")
    return db_banks

def read_bank(db: Session, user_id: str, bank_id: int):
    db_bank = db.query(BankDataModel).filter(BankDataModel.id == bank_id, BankDataModel.user_u_id == user_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank data not found")
    return db_bank

def update_bank(db: Session, user_id: str, bank: BankData):
    db_bank = db.query(BankDataModel).filter(BankDataModel.id == bank.id, BankDataModel.user_u_id == user_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank data not found")
    for key, value in bank.model_dump(exclude_unset=True).items():
        setattr(db_bank, key, value)
    db.commit()
    db.refresh(db_bank)
    return db_bank

def delete_bank(db: Session, user_id: str, bank_id: int):
    db_bank = db.query(BankDataModel).filter(BankDataModel.id == bank_id, BankDataModel.user_u_id == user_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank data not found")
    db.delete(db_bank)
    db.commit()
    return JSONResponse(
        content={"msg": f"Bank data with ID {bank_id} has been deleted successfully."},
        status_code=status.HTTP_200_OK,
    )
