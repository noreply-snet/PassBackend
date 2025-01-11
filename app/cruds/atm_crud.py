from sqlalchemy.orm import Session
from fastapi import HTTPException , status
from fastapi.responses import JSONResponse
from ..models.main_models import AtmDataModel
from ..schemas.atm_schemas import AtmDataCreate, AtmData

def create_atm(db: Session, atm: AtmDataCreate):
    db_atm = AtmDataModel(**atm.model_dump())
    db.add(db_atm)
    db.commit()
    db.refresh(db_atm)
    return db_atm

def read_all_atms(db: Session):
    db_atm = db.query(AtmDataModel).all()
    if not db_atm:
        raise HTTPException(status_code=404, detail="ATMs data not found")
    return db_atm

def read_atm(db: Session, atm_id: int):
    db_atm = db.query(AtmDataModel).filter(AtmDataModel.id == atm_id).first()
    if not db_atm:
        raise HTTPException(status_code=404, detail="ATM data not found")
    return db_atm

def update_atm(db: Session, atm: AtmData):
    db_atm = db.query(AtmDataModel).filter(AtmDataModel.id == atm.id).first()
    if not db_atm:
        raise HTTPException(status_code=404, detail="ATM data not found")
    for key, value in atm.model_dump(exclude_unset=True).items():
        setattr(db_atm, key, value)
    db.commit()
    db.refresh(db_atm)
    return db_atm

def delete_atm(db: Session, atm_id: int):
    db_atm = db.query(AtmDataModel).filter(AtmDataModel.id == atm_id).first()
    if not db_atm:
        raise HTTPException(status_code=404, detail="ATM data not found")
    db.delete(db_atm)
    db.commit()
    return JSONResponse(
        content={"msg": f"ATM data with ID {atm_id} has been deleted successfully."},
        status_code=status.HTTP_200_OK,
    )
