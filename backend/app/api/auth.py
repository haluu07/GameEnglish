from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session, get_current_user
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
)
from app.schemas.common import TokenPair, UserWithStats
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    user, stats, tokens = await service.register(
        email=payload.email,
        password=payload.password,
        display_name=payload.display_name,
    )
    return AuthResponse(
        user=UserWithStats(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            role=user.role,
            created_at=user.created_at,
            stats=stats,
        ),
        tokens=tokens,
    )


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    user, stats, tokens = await service.login(payload.email, payload.password)
    return AuthResponse(
        user=UserWithStats(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            role=user.role,
            created_at=user.created_at,
            stats=stats,
        ),
        tokens=tokens,
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    return await service.refresh_access(payload.refresh_token)


@router.get("/me", response_model=UserWithStats)
async def me(current_user: UserWithStats = Depends(get_current_user)):
    return current_user

