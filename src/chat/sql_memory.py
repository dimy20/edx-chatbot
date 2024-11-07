from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory
#TODO

class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversaton_id : str

    @property
    def messages(self):
        pass