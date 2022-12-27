from sqlalchemy import Boolean, DateTime, Column, Integer, String, PickleType, Text, ForeignKey

from services.database import Base

from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class Entry(Base):
    __tablename__ = 'entries'
    # Entry-specific information
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    user: str = Column(String(36), ForeignKey("users.uuid"), nullable=False, unique=True)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())

    # Data
    text: str = Column(Text, nullable=False)
    flags: list = Column(PickleType, nullable=False, default=[])
    tags: list = Column(PickleType, nullable=False, default=[])

    # Tracking
    read: bool = Column(Boolean, nullable=False, default=False)
    read_at: datetime = Column(DateTime, nullable=True, default=None)

    def __repr__(self):
        return f"<Entry {self.id}>"
