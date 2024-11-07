from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages.base import BaseMessage

from db.db import get_db
from db.models import Conversation, Message

def db_message_to_lang_msg(msg: Message):
    if msg.role == "human":
        return HumanMessage(content=msg.content)
    elif msg.role == "ai":
        return AIMessage(content=msg.content)
    elif msg.role == "system":
        return SystemMessage(content=msg.content)

def role_from_msg(message : BaseMessage):
    if isinstance(message, AIMessage):
        return "ai"
    elif isinstance(message, HumanMessage):
        return "human"
    elif isinstance(message, HumanMessage):
        return "system"

def get_messages_by_conversation_id(conversation_id : str):
    db : Session = next(get_db())
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    ans = []

    for msg in conversation.messages:
        ans.append(db_message_to_lang_msg(msg))

    return ans


def add_message_to_conversation(message_content: str, conversation_id: str, role: str):
    db : Session = next(get_db())
    message_db = Message(content=message_content, conversation_id=conversation_id, role=role)
    db.add(message_db)
    db.commit()
    db.refresh(message_db)
    return message_db
    
class SqlMessageHistory(BaseChatMessageHistory):
    def __init__(self, conversation_id : str):
        self.conversation_id : str = conversation_id

    @property
    def messages(self):
        msgs = get_messages_by_conversation_id(self.conversation_id)
        return msgs

    def add_message(self, message):
        return add_message_to_conversation(
            message_content=message.content,
            conversation_id=self.conversation_id,
            role=role_from_msg(message)
        )

    def clear(self):
        pass

def init_memory(conversation_id: str):
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(conversation_id),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )