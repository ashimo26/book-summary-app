# quiz/quiz_generator.py
import json
import random
from langchain.llms import OpenAI
from vectorstore.store import get_vectorstore
from .quiz_state import set_current_answer, get_current_answer

def generate_quiz_question():
    vectordb = get_vectorstore()
    docs = vectordb._collection.get()["documents"]
    if not docs:
        return "文書がベクトルストアに存在しません。", []

    content = random.choice(docs)
    prompt = (
        "次の文章に基づいて、クイズの質問を1つ作成してください。\n"
        "4つの選択肢 (A, B, C, D) を提示し、正解も指定してください。\n"
        "出力形式はJSONで、question, options, answerをキーとしてください。\n\n"
        f"文章:\n'''{content}'''"
    )
    llm = OpenAI(temperature=0)
    response = llm.predict(prompt)

    try:
        quiz = json.loads(response)
        question = quiz["question"]
        options = quiz["options"]
        answer = quiz["answer"]
        set_current_answer(answer, options)
        return question, options
    except Exception:
        return "クイズの生成に失敗しました。", []

def check_answer(user_choice):
    correct = get_current_answer()
    if not correct:
        return "まず問題を生成してください。"
    if user_choice.strip() == correct.strip():
        return "正解です！ 🎉"
    else:
        return f"不正解です。正解は「{correct}」です。"