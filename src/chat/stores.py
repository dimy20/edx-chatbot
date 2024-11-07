import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from chat.embeddings import embeddings

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"),
              environment=os.getenv("PINECONE_ENV_NAME"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

vector_store = PineconeVectorStore(index=index, embedding=embeddings)


def make_retriever(course_id: str):
    search_kwargs = {
        "filter" : {"course_id": course_id}
    }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )