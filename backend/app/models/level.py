from sqlalchemy import Column, Integer, Numeric, String, Text

from app.core.database import Base


class Level(Base):
    __tablename__ = "levels"

    code = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    unlock_threshold = Column(Integer, nullable=False)
    xp_multiplier = Column(Numeric(3, 2), nullable=False)

