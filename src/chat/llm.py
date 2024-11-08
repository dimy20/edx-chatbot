from langchain_openai.chat_models import ChatOpenAI

def init_llm(streaming: bool):
    return ChatOpenAI(streaming=streaming)