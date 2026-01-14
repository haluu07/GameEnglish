import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    level_code = Column(String(10), ForeignKey("levels.code", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)

    __table_args__ = (
        Index("ix_chapters_level_code_order_index", "level_code", "order_index"),
    )

