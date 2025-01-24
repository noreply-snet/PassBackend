from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core import security
from ...database.session import get_db
from ...cruds import user_crud as crud
from ...schemas import user_schemas as schemas

router = APIRouter()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user


lockedRouter = APIRouter(
    dependencies=[Depends(security.get_current_user)],
)

@lockedRouter.get("/", response_model=List[schemas.UserResponse])
def read_all_users(db: Session = Depends(get_db)):
    users = crud.read_all_users(db)
    return users

@lockedRouter.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = crud.read_user(db, user_id)
    return user

@lockedRouter.put("/update/email", response_model=schemas.UserResponse)
def update_user_email(user: schemas.UserUpdateEmail, db: Session = Depends(get_db)):
    db_user = crud.update_user_email(db,user)
    return db_user

@lockedRouter.put("/update/password", response_model=schemas.UserResponse)
def update_user_pass(user: schemas.UserUpdatePassword, db: Session = Depends(get_db)):
    db_user = crud.update_user_password(db, user)
    return db_user

router.include_router(lockedRouter)


