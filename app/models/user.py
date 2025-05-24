from sqlalchemy import Boolean, Column, String, Enum
from app.models.base import Base
import enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False) 