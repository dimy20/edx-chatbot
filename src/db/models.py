# models.py
from db.db import Base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="courses")

    conversations = relationship(
        "Conversation",
        back_populates="course",
        order_by="desc(Conversation.created_on)"
    )

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    created_on = Column(DateTime, default=datetime.now())
    retriever = Column(String)
    memory = Column(String)
    llm = Column(String)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="conversations")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="conversations")

    messages = relationship(
        "Message", back_populates="conversation", order_by="Message.created_on"
    )

    def as_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "messages": [message.as_dict() for message in self.messages],
        }

class Message(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    created_on = Column(DateTime, default=datetime.now())
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)

    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    conversation = relationship("Conversation", back_populates="messages")

    def as_dict(self):
        return {"id": self.id, "role": self.role, "content": self.content}

    def as_lc_message(self):
        from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage

        if self.role == "human":
            return HumanMessage(content=self.content)
        elif self.role == "ai":
            return AIMessage(content=self.content)
        elif self.role == "system":
            return SystemMessage(content=self.content)
        else:
            raise ValueError(f"Unknown message role: {self.role}")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(80), unique=True, nullable=False)
    name = Column(String(80), unique=False, nullable=False)
    password = Column(String(80), nullable=False)

    courses = relationship("Course", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")

    def as_dict(self):
        return {"id": self.id, "name" : self.name, "email": self.email}