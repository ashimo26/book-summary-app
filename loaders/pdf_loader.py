# loaders/pdf_loader.py
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from vectorstore.store import get_vectorstore

def add_pdf_to_vectorstore(pdf_file):
    vectordb = get_vectorstore()
    loader = PyPDFLoader(pdf_file.name)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)
    vectordb.add_documents(docs)
    return f"{len(docs)}個の文書チャンクをベクトルストアに保存しました。"