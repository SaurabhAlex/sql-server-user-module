from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class UserCustom(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    u_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=True)
    mobile_no = Column(String(15), nullable=True)
    role_id = Column(Integer, nullable=True)
    u_password = Column(LargeBinary, nullable=False)

    def __repr__(self):
        return f"<UserCustom(u_name={self.u_name}, email={self.email})>"
