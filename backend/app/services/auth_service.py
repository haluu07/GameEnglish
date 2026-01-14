from typing import Tuple
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserStats, UserRoleEnum
from app.schemas.common import UserWithStats, TokenPair


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_user_by_email(self, email: str) -> User | None:
        res = await self.db.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    async def register(self, email: str, password: str, display_name: str) -> Tuple[User, UserStats, TokenPair]:
        existing = await self._get_user_by_email(email)
        if existing:
            raise exceptions.bad_request("Email already registered")

        user = User(
            email=email,
            display_name=display_name,
            password_hash=hash_password(password),
            role=UserRoleEnum.USER,
        )
        stats = UserStats(user_id=user.id)

        self.db.add(user)
        self.db.add(stats)
        await self.db.commit()
        await self.db.refresh(user)
        await self.db.refresh(stats)

        tokens = TokenPair(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )
        return user, stats, tokens

    async def login(self, email: str, password: str) -> Tuple[User, UserStats, TokenPair]:
        user = await self._get_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise exceptions.unauthorized("Invalid credentials")

        stats = await self._get_user_stats(user.id)
        tokens = TokenPair(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )
        return user, stats, tokens

    async def refresh_access(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_token(refresh_token)
        except ValueError:
            raise exceptions.unauthorized("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise exceptions.unauthorized("Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise exceptions.unauthorized("Invalid token payload")

        new_access = create_access_token(str(user_id))
        return TokenPair(access_token=new_access, refresh_token=refresh_token)

    async def _get_user_stats(self, user_id: UUID) -> UserStats:
        res = await self.db.execute(select(UserStats).where(UserStats.user_id == user_id))
        stats = res.scalar_one_or_none()
        if not stats:
            stats = UserStats(user_id=user_id)
            self.db.add(stats)
            await self.db.commit()
            await self.db.refresh(stats)
        return stats

    async def get_current_user_with_stats(self, user_id: UUID) -> UserWithStats:
        res = await self.db.execute(select(User).where(User.id == user_id))
        user = res.scalar_one_or_none()
        if not user:
            raise exceptions.unauthorized("User not found")
        stats = await self._get_user_stats(user.id)
        return UserWithStats(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            role=user.role,
            created_at=user.created_at,
            stats=stats,
        )

