from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Enum
from app.models.base import Base
import enum


class LogLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Log(Base):
    level = Column(Enum(LogLevel), nullable=False)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    action = Column(String, nullable=False)  # e.g., "user_login", "order_create"
    details = Column(JSON, nullable=True)  # Additional context as JSON 