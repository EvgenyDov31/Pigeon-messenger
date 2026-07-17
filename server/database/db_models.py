"""
Консольный мессенджер.

Модели для БД
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(String, unique=True, nullable=False)
        username = Column(String, nullable=False)
        password_hash = Column(Text, nullable=False)