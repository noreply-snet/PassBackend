from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..cruds import user_crud as crud
from ..schemas import user_schemas as schemas

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user

@router.get("/users/", response_model=List[schemas.UserResponse])
def read_all_users(db: Session = Depends(get_db)):
    users = crud.read_all_users(db)
    return users

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = crud.read_user(db, user_id)
    return user

@router.put("/users/update/email", response_model=schemas.UserResponse)
def update_user_email(user: schemas.UserUpdateEmail, db: Session = Depends(get_db)):
    db_user = crud.update_user_email(db,user)
    return db_user

@router.put("/users/update/password", response_model=schemas.UserResponse)
def update_user_pass(user: schemas.UserUpdatePassword, db: Session = Depends(get_db)):
    db_user = crud.update_user_password(db, user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)
