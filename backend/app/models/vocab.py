import uuid

from sqlalchemy import Column, ForeignKey, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Vocab(Base):
    __tablename__ = "vocab"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id = Column(
        UUID(as_uuid=True),
        ForeignKey("missions.id", ondelete="CASCADE"),
        nullable=False,
    )
    word = Column(String(255), nullable=False)
    ipa = Column(String(255), nullable=True)
    meaning_vi = Column(String(255), nullable=False)
    example_en = Column(Text, nullable=False)

    __table_args__ = (
        Index("ix_vocab_mission_id", "mission_id"),
    )

