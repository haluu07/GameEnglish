import uuid

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class UserRoleEnum(str):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum(UserRoleEnum.USER, UserRoleEnum.ADMIN, name="user_role"),
        nullable=False,
        server_default=UserRoleEnum.USER,
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class UserStats(Base):
    __tablename__ = "user_stats"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    xp_total = Column(Integer, nullable=False, server_default="0")
    streak_count = Column(Integer, nullable=False, server_default="0")
    last_active_date = Column(Date, nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

