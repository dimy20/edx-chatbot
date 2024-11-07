from pydantic import BaseModel

class MetaData(BaseModel):
    conversation_id : str
    user_id : str
    course_id: str

class ChatArgs(BaseModel):
    converstaion_id : str
    course_id: str
    metadata: MetaData
    streaming: bool