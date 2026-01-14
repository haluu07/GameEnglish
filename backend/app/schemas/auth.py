from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import TokenPair, UserWithStats


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    display_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class AuthResponse(BaseModel):
    user: UserWithStats
    tokens: TokenPair

