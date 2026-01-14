from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core import exceptions
from app.core.security import decode_token
from app.services.auth_service import AuthService


async def get_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db


async def get_current_user_id(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> UUID:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise exceptions.unauthorized("Missing Authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except ValueError:
        raise exceptions.unauthorized("Invalid token")
    if payload.get("type") != "access":
        raise exceptions.unauthorized("Invalid token type")
    sub = payload.get("sub")
    if not sub:
        raise exceptions.unauthorized("Invalid token payload")
    return UUID(sub)


async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(db)
    return await auth_service.get_current_user_with_stats(user_id)

