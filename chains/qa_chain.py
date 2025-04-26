# chains/qa_chain.py
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from vectorstore.store import get_vectorstore
import os
import shutil

def answer_question(query, doc_id):
    vectordb = get_vectorstore(doc_id)
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model="gpt-4o",temperature=0), chain_type="stuff", retriever=retriever)
    return qa.run(query)

def delete_doc(doc_id):
    persist_dir = os.path.join("chroma_store", doc_id)
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)  # ディレクトリを再帰的に削除
        return f"'{doc_id}' フォルダが削除されました。"
    else:
        return f"エラー: '{doc_id}' フォルダは存在しません。"