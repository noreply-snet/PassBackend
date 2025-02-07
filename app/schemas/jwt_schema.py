from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str

class JWTPayload(BaseModel):
    sub: str
    exp: datetime
    jti: str