from sqlalchemy import Boolean, DateTime, Column, Integer, String, PickleType
from sqlalchemy.orm import relationship

from services.utilities import Utilities
from services.database import Base

from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class User(Base):
    """
    User model representing a user.\n
    This is either an admin, allowing to make changes to the microservice.\n
    But usually someone that is able to see products, events and orders to place new orders.
    """
    # TODO: Add methods to make database changes easier.
    __tablename__ = 'users'
    # User-specific information
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    username: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(50), nullable=False, unique=True)
    email: str = Column(String(50), nullable=False, unique=True)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    country: str = Column(String(20), nullable=True, default="NL")
    children = relationship("Entry")

    # Clearance/security/authentication
    flags: list = Column(PickleType, nullable=False, default=[])
    admin: bool = Column(Boolean, nullable=False, default=False)
    password: str = Column(String(200), nullable=False)
    secret: str = Column(String(50), nullable=True, unique=True, default=Utilities.generate_secret())
    token: str = Column(String(500), nullable=True, unique=True, default=None)
    tags: list = Column(PickleType, nullable=False, default=[])

    def get_fullname(self):
        return f"{self.name[0]}. {self.name.split(' ')[1]}"

    def __repr__(self):
        return f"<User {self.get_fullname()}>"
