from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
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
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate tokens using your jwt_manager;
    access_token, refresh_token = jwt_manager.generate_tokens(user.u_id)
    
    # Set the refresh token in an HttpOnly, Secure cookie with SameSite set to "strict"
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,       # Prevents JavaScript access
        expires=datetime.now(timezone.utc) + timedelta(days=30), # Set cookie expiration
        secure=True,         # Only send cookie over HTTPS
        samesite="strict"     # Restricts cross-site sending of cookie
    )
    # Return the access token (refresh token remains in the cookie)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    response: Response,
    db: Session = Depends(get_db),
    # refresh_token: str = Cookie(None)  # Read the refresh token from cookie
    refresh_token: str = Cookie(None)  # Read the refresh token from cookie
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    # Verify the refresh token (assume verify_token returns the decoded payload)
    payload = jwt_manager.verify_token(db=db, token=refresh_token)
    user = db.query(User).filter(User.u_id == payload["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate new tokens
    new_access_token, new_refresh_token = jwt_manager.generate_tokens(user.u_id)
    # Update the refresh token cookie with the new token
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        expires=datetime.now(timezone.utc) + timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="strict"
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


# Routes that require authentication
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
        raise HTTPException(status_code=500, detail=str(e))


@lockRouter.post("/logout")
def logout(
    response: Response,
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Verify the provided access token
    payload = security.jwt_manager.verify_token(db=db, token=token)
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    # Revoke the token (using your revoke_token function)
    revoke_token(db=db, token_id=payload["jti"], expires_at=expires_at)
    # Clear the refresh token cookie by deleting it
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}


router.include_router(lockRouter)
