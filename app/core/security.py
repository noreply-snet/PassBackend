# security.py
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.utills import verify_password
from app.services.jwt import jwt_manager
from app.cruds import user_crud
from app.database.session import get_db
from app.models.user_models import User, Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Authenticate the user with additional checks
def authenticate_user(db: Session, username: str, password: str):
    user: User = user_crud.read_user_by_email(
        db, username, 
        # Eager load relationships to optimize permission checks
        options=[joinedload(User.roles).joinedload(Role.permissions)]
    )
    
    # Check account existence, activation, and password
    if not user or not user.is_active or not verify_password(password, user.password):
        return False
    return user

# Get current user with authorization checks
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt_manager.verify_token(db=db, token=token)
    user: User = user_crud.read_user(
        db, payload["sub"],
        options=[joinedload(User.roles).joinedload(Role.permissions)]
    )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account"
        )
    return user

# Authorization dependencies
def require_superuser(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser privileges required"
        )
    return user

def require_staff(user: User = Depends(get_current_user)):
    if not user.is_staff and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff privileges required"
        )
    return user

def has_permission(user: User, required_permission: str) -> bool:
    if user.is_superuser:
        return True
    return any(
        permission.name == required_permission
        for role in user.roles
        for permission in role.permissions
    )

def require_permission(permission: str):
    def dependency(user: User = Depends(get_current_user)):
        if not has_permission(user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires '{permission}' permission"
            )
        return user
    return dependency

# Helper function remains the same
def get_current_user_id(user: User = Depends(get_current_user)):
    return user.u_id