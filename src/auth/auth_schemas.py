from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    refresh_token: str|None = None
    token_type: str = "Bearer"

class TokenData(BaseModel):
    email: EmailStr
    type: str