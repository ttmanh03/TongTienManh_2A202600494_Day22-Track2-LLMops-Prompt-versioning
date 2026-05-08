import os
from pathlib import Path
from dotenv import load_dotenv
# Load .env từ thư mục gốc
load_dotenv(Path(__file__).parent / ".env")

# Bắt buộc phải set TRƯỚC khi import LangChain
os.environ["LANGCHAIN_TRACING_V2"]  = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_API_KEY"]     = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"]     = os.getenv("LANGCHAIN_PROJECT", "day22-lab")
os.environ["LANGCHAIN_ENDPOINT"]    = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL   = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL         = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL   = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LANGSMITH_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")

if __name__ == "__main__":
    print("✅ Config loaded successfully")
    print(f"   LangSmith project : {os.environ['LANGCHAIN_PROJECT']}")
    print(f"   OpenAI endpoint   : {OPENAI_BASE_URL}")
    print(f"   Default LLM model : {LLM_MODEL}")
    print(f"   Embedding model   : {EMBEDDING_MODEL}")