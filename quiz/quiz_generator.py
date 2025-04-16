from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from pydantic import BaseModel, Field
import random
from vectorstore.store import get_vectorstore
from .quiz_state import set_current_answer, get_current_answer
from gradio import update

# Step 1: クイズのスキーマを定義
class Quiz(BaseModel):
    question: str = Field(description="クイズの質問文")
    options: list[str] = Field(description="選択肢 A〜D のリスト")
    answer: str = Field(description="正解（A, B, C, D のいずれか）")

# Step 2: パーサーを作成
parser = PydanticOutputParser(pydantic_object=Quiz)

# Step 3: プロンプトテンプレート
prompt_template = PromptTemplate(
    template=(
        "次の文章に基づいて、4択のクイズを1問作成してください。\n"
        "クイズは以下の形式で出力してください（これは例ではなく、正確なJSON構造で返してください）：\n\n"
        "{{\n"
        "  \"question\": \"クイズの質問文\",\n"
        "  \"options\": [\"選択肢A\", \"選択肢B\", \"選択肢C\", \"選択肢D\"],\n"
        "  \"answer\": \"A\"\n"
        "}}\n\n"
        "文章：\n'''{content}'''\n"
    ),
    input_variables=["content"],
    partial_variables={}
)

def generate_quiz_question():
    vectordb = get_vectorstore()
    docs = vectordb._collection.get()["documents"]
    if not docs:
        return "ベクトルストアに文書がありません。", []

    content = random.choice(docs)
    llm = OpenAI(temperature=0)
    prompt = prompt_template.format(content=content)
    response = llm.predict(prompt)

    try:
        quiz: Quiz = parser.parse(response)
        set_current_answer(quiz.answer, quiz.options)
        return quiz.question, update(choices=quiz.options, value=None)
    except Exception as e:
        return f"❌ クイズの構造解析に失敗しました: {e}", []

def check_answer(user_choice):
    correct = get_current_answer()
    if not correct:
        return "まず問題を生成してください。"
    if user_choice.strip() == correct.strip():
        return "正解です！ 🎉"
    else:
        return f"不正解です。正解は「{correct}」です。"