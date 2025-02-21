from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)

    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    avatar_color: str = Column(String, nullable=False)

    slides = relationship("Slide", back_populates="owner", lazy="joined")
