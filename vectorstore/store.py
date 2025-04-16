# vectorstore/store.py
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

_vectordb = None

def get_vectorstore():
    global _vectordb
    if _vectordb is None:
        _vectordb = Chroma(collection_name="documents", embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_store")
    return _vectordb