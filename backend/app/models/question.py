import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mission_id = Column(
        UUID(as_uuid=True),
        ForeignKey("missions.id", ondelete="CASCADE"),
        nullable=False,
    )
    type = Column(String(32), nullable=False)  # MCQ | FILL_BLANK | LISTEN_PICK | REORDER | SHORT_ANSWER
    prompt = Column(Text, nullable=False)
    choices = Column(JSONB, nullable=True)
    answer = Column(JSONB, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Integer, nullable=False)

    __table_args__ = (
        Index("ix_questions_mission_id", "mission_id"),
    )

