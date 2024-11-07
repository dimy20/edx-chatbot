from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from chat.stores import vector_store, make_retriever

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

def build_chat(course_id: str):
    print(f"building chat for {course_id}")