# engine/api/public/db/models.py
from sqlalchemy import Column, String, Integer, Boolean, SmallInteger, TIMESTAMP, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False, default=generate_uuid)  # UUID Minecraft style
    nickname = Column(String(16), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Boolean, nullable=False, default=True)
    verify = Column(SmallInteger, nullable=False, default=0)
    verify_token = Column(String(255), nullable=True)
    verification_expiry = Column(TIMESTAMP, nullable=True)
    last_password_change = Column(TIMESTAMP, nullable=True)
    failed_login_attempts = Column(Integer, nullable=False, default=0)
    last_login = Column(TIMESTAMP, nullable=True)
    last_login_ip = Column(String(45), nullable=True)  # IPv6 compatible
    bio = Column(Text, nullable=True)
    timezone = Column(String(50), nullable=True)
    profile_picture_url = Column(String(255), nullable=True)
    skin_url = Column(String(255), nullable=True)
    cape_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
