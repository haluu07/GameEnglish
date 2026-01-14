from datetime import datetime, date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    role: Literal["user", "admin"]
    created_at: datetime


class UserStatsOut(BaseModel):
    xp_total: int
    streak_count: int
    last_active_date: Optional[date] = None
    updated_at: datetime


class UserWithStats(UserBase):
    stats: UserStatsOut


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

