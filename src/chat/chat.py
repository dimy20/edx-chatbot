from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain


from chat.stores import vector_store, init_retriever
from chat.llm import init_llm
from chat.sql_memory import init_memory

def gen_overview_embeddings(overview_text: str, course_id: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(overview_text)
    n = len(chunks)
    docs : List[Document] = [None] * n

    metadata = {
        "course_id" : course_id
    }

    for i in range(n):
        docs[i] = Document(page_content=chunks[i], metadata=metadata)
    
    return vector_store.add_documents(docs)

def init_chat(course_id: str, conversation_id: str):
    retriever = init_retriever(course_id)
    llm = init_llm()
    mem = init_memory(conversation_id)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=mem,
        retriever=retriever,
    )