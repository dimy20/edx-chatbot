from typing import List

from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from chat.stores import vector_store

def gen_overview_embeddings(overview_text: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(overview_text)
    n = len(chunks)
    docs : List[Document] = [None] * n

    for i in range(n):
        docs[i] = Document(page_content=chunks[i])
    
    return vector_store.add_documents(docs)

