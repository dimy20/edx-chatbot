from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.models import Conversation, Course, User
from db.db import get_db
from typing import Optional
from chat.chat import build_chat


router = APIRouter()
PREFIX= "/api/v1/conversations"

def load_conversation(conversation_id : str, db : Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

class ConversationCreate(BaseModel):
    retriever: str | None = None
    memory: str | None = None
    llm: str | None = None
    course_name: str
    user_id: str

@router.post("/")
async def create_conversation(conversation: ConversationCreate, db : Session = Depends(get_db)):
    course = db.query(Course).filter(Course.name == conversation.course_name).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"No se ha procesado el curso : {conversation.course_name}")

    new_conv = Conversation(course_id=course.id, user_id=conversation.user_id)
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)

    return {
        "Status" : "Success",
        "conversation_added" : new_conv.as_dict()
    }

class MessageCreate(BaseModel):
    content: str
    user_id : str

@router.post("/{conversation_id}/messages")
async def create_message(conversation_id : str, 
                         message: MessageCreate,
                         db : Session = Depends(get_db),
                         conversation: Conversation = Depends(load_conversation),
                         streaming: Optional[bool] = False):
    
    #Provisorio, cambiar cuando tengamos login implementado
    user = db.query(User).filter(User.id == message.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id {message.user_id}, doesnt exist")

    course = conversation.course
    build_chat(course.id)
    # Build chat arguments
    return {
        "status" : "Success",
        "message_added" : message.content,
        "conversation" : conversation.as_dict(), 
    }

@router.get("/")
async def get_conversations(db : Session = Depends(get_db)):
    return db.query(Conversation).all()
