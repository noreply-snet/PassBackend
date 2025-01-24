from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import uuid
from app.cruds.jwt_crud import is_token_revoked
from app.core.config import jwt_settings as settings

class JWTManager:
    def generate_tokens(self, user_id: str):
        jwt_id = str(uuid.uuid4())
        access_token = self.create_token(
            data={"sub": user_id}, token_type="access", jwi=jwt_id
        )
        refresh_token = self.create_token(
            data={"sub": user_id}, token_type="refresh", jwi=jwt_id
        )
        return access_token, refresh_token

    @staticmethod
    def create_token(data: dict, token_type: str, jwi: str = None) -> str:
        to_encode = data.copy()
        if token_type == "access":
            expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_EXPIRE)
        elif token_type == "refresh":
            expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_EXPIRE)
        else:
            raise ValueError("Invalid token type. Must be 'access' or 'refresh'.")
        
        to_encode.update({"exp": expire, "jti": jwi})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET, algorithm=settings.ALGO)
        return encoded_jwt

    def verify_token(self, db: Session, token: str):
        excp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGO])
            
            if is_token_revoked(db, payload["jti"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            if "exp" in payload and datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz=timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_id: str = payload.get("sub")
            if user_id is None:
                raise excp

            return payload
        except JWTError:
            raise excp

jwt_manager = JWTManager()  # Create an instance of JWTManager
