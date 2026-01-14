import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Mission(Base):
    __tablename__ = "missions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    xp_reward = Column(Integer, nullable=False, server_default="100")
    map_key = Column(String(100), nullable=False)

    __table_args__ = (
        Index("ix_missions_chapter_id_order_index", "chapter_id", "order_index"),
    )

