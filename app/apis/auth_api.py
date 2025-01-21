from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.jwt import jwt_manager
from app.schemas.jwt_schema import Token
from app.database.session import get_db
from app.core import security
from app.cruds.jwt_crud import cleanup_expired_tokens, get_expired_tokens, revoke_token
from app.models.main_models import User  # Import the User model

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if user is None :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, refresh_token = jwt_manager.generate_tokens(user.u_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(db: Session = Depends(get_db), refresh_token: str = ""):
    payload = jwt_manager.verify_token(db=db, token=refresh_token)
    user = db.query(User).filter(User.u_id == payload["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_access_token, new_refresh_token = jwt_manager.generate_tokens(user.u_id)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


lockRouter = APIRouter(
    dependencies=[Depends(security.get_current_user)],
)




@lockRouter.get("/cleanup-tokens")
def cleanup_token(db: Session = Depends(get_db)):
    cleanup_expired_tokens(db)
    return {"message": "Expired tokens cleaned up successfully."}


@lockRouter.get("/exp-tokens")
def get_exp_token(db: Session = Depends(get_db)):
    try:
        return get_expired_tokens(db)
    except Exception as e:
        # Log the exception if necessary
        raise HTTPException(status_code=500, detail=str(e))

@lockRouter.post("/logout")
def logout(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.jwt_manager.verify_token(db=db, token=token)
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    revoke_token(db=db, token_id=payload["jti"], expires_at=expires_at)
    return {"message": "Logged out successfully"}