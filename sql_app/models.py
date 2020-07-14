from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


# 数据库模型
# 用户表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    avatar = Column(String, default=None)
    hashed_password = Column(String)
    role = Column(String, default="general")
    is_active = Column(Boolean, default=True)

    todos = relationship("ToDo", back_populates="owner_todo")


# TODO表
class ToDo(Base):
    __tablename__ = "todo_info"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    done = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner_todo = relationship("User", back_populates="todos")
