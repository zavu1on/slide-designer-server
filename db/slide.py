from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Slide(Base):
    __tablename__ = "slides"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid: str = Column(String, index=True, unique=True, nullable=False)
    name: str = Column(String, nullable=False)
    update_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    data: str = Column(Text)

    user_id: int = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="slides")
