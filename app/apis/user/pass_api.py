from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core import security
from ...database.session import get_db
from ...cruds.pass_crud import create_password, read_password, update_password, delete_password, read_all_passwords
from ...schemas.pass_schemas import PassDataCreate, PassData
from typing import List

router = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)

@router.post("/", response_model=PassData)
def create_password_route(password: PassDataCreate, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return create_password(db, user_id, password)

@router.get("/all", response_model=List[PassData])
def read_all_notes_route(db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return read_all_passwords(db, user_id)

@router.get("/{password_id}", response_model=PassData)
def read_password_route(password_id: int, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return read_password(db, user_id, password_id)

@router.put("/", response_model=PassData)
def update_password_route(password: PassData, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return update_password(db, user_id, password)

@router.delete("/{password_id}")
def delete_password_route(password_id: int, db: Session = Depends(get_db), user_id: str = Depends(security.get_current_user_id)):
    return delete_password(db, user_id, password_id)
