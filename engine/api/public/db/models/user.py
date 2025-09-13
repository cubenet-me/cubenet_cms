# engine/api/public/db/models/user.py
from sqlalchemy import Column, Integer, String
from engine.api.public.db.connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String)
