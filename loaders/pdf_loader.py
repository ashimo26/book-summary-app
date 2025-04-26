# loaders/pdf_loader.py
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from vectorstore.store import create_vectorstore
import pdfplumber
import pytesseract
from langchain.schema import Document
from PIL import Image
import platform
import os

def add_pdf_to_vectorstore(pdf_file, text_option):
    doc_id = os.path.splitext(os.path.basename(pdf_file.name))[0]
    vectordb = create_vectorstore(doc_id)
    loader = PyPDFLoader(pdf_file.name)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents_text = extract_text_from_pdf(pdf_file, text_option)
    docs = splitter.split_documents(documents_text)
    vectordb.add_documents(docs)
    return f"{len(docs)}個の文書チャンクをベクトルストアに保存しました。"

# PDFからOCRを使ってテキストを抽出する関数
def extract_text_from_pdf(pdf_file, text_option):
    pages = []
    if(text_option == '横文字'):
        lang = 'jpn'
        custom_config = '--psm 6'
    else:
        lang = 'jpn+jpn_vert'
        custom_config = '--psm 5'
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            # 進捗を表示
            progress = (i + 1) / total_pages * 100
            print(f"[{'█' * int((progress//5))}{' ' * int((20 - progress//5))}] {progress}% 完了")
            # 画像としてページを取得
            image = page.to_image()
            # OCRを使用して画像からテキストを抽出
            text = pytesseract.image_to_string(image.original, lang=lang, config=custom_config)
            print(text)
            pages.append(Document(page_content=text))
    return pages