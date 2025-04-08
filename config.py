# config.py
from dotenv import load_dotenv
import os

# .envファイルを読み込む
load_dotenv()

# OpenAI APIキーを環境変数から取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY が .env に設定されていません")