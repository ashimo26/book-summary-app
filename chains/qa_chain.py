# chains/qa_chain.py
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from vectorstore.store import get_vectorstore

def answer_question(query):
    vectordb = get_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0), chain_type="stuff", retriever=retriever)
    return qa.run(query)