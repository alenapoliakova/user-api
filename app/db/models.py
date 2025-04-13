from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    patronymic = Column(String(64), nullable=True)
    password_hash = Column(String(255), nullable=False)
    type = Column(String(16), nullable=False)
    class_name = Column(String(8), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    subject = Column(String(64), nullable=True)
