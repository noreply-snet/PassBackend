from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from ..models.main_models import BankDataModel
from ..schemas.bank_schemas import BankDataCreate, BankDataUpdate

def create_bank(db: Session, bank: BankDataCreate):
    db_bank = BankDataModel(**bank.model_dump())
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

def read_all_banks(db: Session):
    db_bank = db.query(BankDataModel).all()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Banks data not found")
    return db_bank

def read_bank(db: Session, bank_id: int):
    db_bank = db.query(BankDataModel).filter(BankDataModel.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank data not found")
    return db_bank

def update_bank(db: Session, bank: BankDataUpdate):
    db_bank = db.query(BankDataModel).filter(BankDataModel.id == bank.id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank data not found")
    for key, value in bank.model_dump(exclude_unset=True).items():
        setattr(db_bank, key, value)
    db.commit()
    db.refresh(db_bank)
    return db_bank

def delete_bank(db: Session, bank_id: int):
    db_bank = db.query(BankDataModel).filter(BankDataModel.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank data not found")
    db.delete(db_bank)
    db.commit()
    return JSONResponse(
        content={"msg": f"Bank data with ID {bank_id} has been deleted successfully."},
        status_code=status.HTTP_200_OK,
    )
