from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.utills import verify_password
from app.services.jwt import jwt_manager
from app.cruds import user_crud
from app.database.session import get_db
from app.models.main_models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Authenticate the user by verifying the password
def authenticate_user(db: Session, username: str, password: str):
    user: User = user_crud.read_user_by_email(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user

# Get the current user from the token
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt_manager.verify_token(db=db, token=token)
    user: User = user_crud.read_user(db, payload["sub"])
    return user


def get_current_user_id(user: User = Depends(get_current_user)):
    return user.u_id