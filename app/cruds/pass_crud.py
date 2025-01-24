from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from ..models.main_models import PassDataModel
from ..schemas.pass_schemas import PassDataCreate, PassData

def create_password(db: Session, user_id: str, password: PassDataCreate):
    db_password = PassDataModel(**password.model_dump(), user_u_id=user_id)
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


def read_all_passwords(db: Session, user_id: str):
    db_passwords = db.query(PassDataModel).filter(PassDataModel.user_u_id == user_id).all()
    if not db_passwords:
        raise HTTPException(status_code=404, detail="Passwords data not found")
    return db_passwords

def read_password(db: Session, user_id: str, password_id: int):
    db_password = db.query(PassDataModel).filter(PassDataModel.id == password_id, PassDataModel.user_u_id == user_id).first()
    if not db_password:
        raise HTTPException(status_code=404, detail="Password data not found")
    return db_password

def update_password(db: Session, user_id: str, password: PassData):
    db_password = db.query(PassDataModel).filter(PassDataModel.id == password.id, PassDataModel.user_u_id == user_id).first()
    if not db_password:
        raise HTTPException(status_code=404, detail="Password data not found")
    for key, value in password.model_dump(exclude_unset=True).items():
        setattr(db_password, key, value)
    db.commit()
    db.refresh(db_password)
    return db_password

def delete_password(db: Session, user_id: str, password_id: int):
    db_password = db.query(PassDataModel).filter(PassDataModel.id == password_id, PassDataModel.user_u_id == user_id).first()
    if not db_password:
        raise HTTPException(status_code=404, detail="Password data not found")
    db.delete(db_password)
    db.commit()
    return JSONResponse(
        content={"msg": f"Password data with ID {password_id} has been deleted successfully."},
        status_code=status.HTTP_200_OK,
    )
