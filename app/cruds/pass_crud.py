from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.main_models import PassDataModel
from schemas.pass_schemas import PassDataCreate, PassDataUpdate

def create_password(db: Session, password: PassDataCreate):
    db_password = PassDataModel(**password.model_dump())
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password

def read_password(db: Session, password_id: int):
    db_password = db.query(PassDataModel).filter(PassDataModel.id == password_id).first()
    if not db_password:
        raise HTTPException(status_code=404, detail="Password data not found")
    return db_password

def update_password(db: Session, password_id: int, password: PassDataUpdate):
    db_password = db.query(PassDataModel).filter(PassDataModel.id == password_id).first()
    if not db_password:
        raise HTTPException(status_code=404, detail="Password data not found")
    for key, value in password.model_dump(exclude_unset=True).items():
        setattr(db_password, key, value)
    db.commit()
    db.refresh(db_password)
    return db_password

def delete_password(db: Session, password_id: int):
    db_password = db.query(PassDataModel).filter(PassDataModel.id == password_id).first()
    if not db_password:
        raise HTTPException(status_code=404, detail="Password data not found")
    db.delete(db_password)
    db.commit()
    return db_password
