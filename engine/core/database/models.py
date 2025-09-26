# engine/core/database/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, INET
from datetime import datetime
import uuid
from .database import Base  # базовый класс из database.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="viewer")
    ip = Column(INET, nullable=True)
    hd = Column(Boolean, default=False, nullable=False)
    money = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    activate_token = Column(String(64), nullable=True)
    is_activate = Column(Boolean, default=False, nullable=False)
