from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from googletrans import Translator
import asyncio
import os

_vectordb = None

def get_vectorstore(doc_id):
    translator = Translator()

    async def translate_doc_id():
        result = await translator.translate(doc_id, dest='en')
        return result.text.replace(" ", "_")
    
    translated_doc_id = asyncio.run(translate_doc_id())

    persist_dir = os.path.join("chroma_store", translated_doc_id)
    os.makedirs(persist_dir, exist_ok=True)

    # 既存のベクトルストアを確認
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        raise ValueError(f"'{translated_doc_id}' はすでに存在します。重複を避けるために別のIDを使用してください。")

    return Chroma(
        collection_name=translated_doc_id,
        embedding_function=OpenAIEmbeddings(),
        persist_directory=persist_dir
    )