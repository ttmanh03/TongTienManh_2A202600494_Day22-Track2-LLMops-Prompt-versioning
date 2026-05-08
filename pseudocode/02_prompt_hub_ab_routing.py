"""
Step 2 — Prompt Hub & A/B Routing
===================================
TASK:
  1. Write two distinct system prompts (V1: concise, V2: structured)
  2. Push both to LangSmith Prompt Hub via client.push_prompt()
  3. Pull them back via client.pull_prompt()
  4. Implement deterministic A/B routing: hash(request_id) % 2 -> V1 or V2
  5. Run all 50 questions through the router -> >= 50 more LangSmith traces

DELIVERABLE: 2 named prompts visible in https://smith.langchain.com Prompt Hub
"""

import os
import sys
import hashlib
from pathlib import Path
from collections import Counter

# ── 1. Environment setup ────────────────────────────────────────────────────
# QUAN TRONG: load .env va set env vars TRUOC KHI import LangChain
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_API_KEY"]    = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"]    = os.getenv("LANGCHAIN_PROJECT", "day22-lab")
os.environ["LANGCHAIN_ENDPOINT"]   = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

# ── 2. Imports ───────────────────────────────────────────────────────────────
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langsmith import Client, traceable

# ── 3. Define two prompt templates ──────────────────────────────────────────
# V1: concise, 2-4 sentences — phong cach ngan gon
SYSTEM_V1 = (
    "You are a helpful AI assistant. "
    "Answer the user's question using ONLY the provided context. "
    "Keep your answer concise (2-4 sentences). "
    "If the context does not contain the answer, say: "
    "'I don't have enough information.'\n\n"
    "Context:\n{context}"
)
PROMPT_V1 = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_V1),
    ("human",  "{question}"),
])

# V2: structured, expert 3-5 sentences — phong cach chi tiet co cau truc
SYSTEM_V2 = (
    "You are an expert AI tutor. Provide a structured, accurate answer.\n\n"
    "Instructions:\n"
    "1. Read the context carefully.\n"
    "2. Identify the key facts relevant to the question.\n"
    "3. Write a clear, well-organized answer (3-5 sentences).\n"
    "4. State explicitly if the context lacks sufficient information.\n\n"
    "Context:\n{context}"
)
PROMPT_V2 = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_V2),
    ("human",  "{question}"),
])

# Ten prompt tren LangSmith Prompt Hub
PROMPT_V1_NAME = "rag-prompt-v1"
PROMPT_V2_NAME = "rag-prompt-v2"


# ── 4. Push prompts to LangSmith Prompt Hub ──────────────────────────────────
def push_prompts_to_hub(client: Client) -> None:
    """Upload both prompt versions to LangSmith Prompt Hub."""
    for name, prompt, desc in [
        (PROMPT_V1_NAME, PROMPT_V1, "V1 - concise answers (2-4 sentences)"),
        (PROMPT_V2_NAME, PROMPT_V2, "V2 - structured expert answers (3-5 sentences)"),
    ]:
        try:
            url = client.push_prompt(name, object=prompt, description=desc)
            print(f"  Pushed {name} -> {url}")
        except Exception as e:
            print(f"  WARNING {name}: {e}")


# ── 5. Pull prompts from Prompt Hub ─────────────────────────────────────────
def pull_prompts_from_hub(client: Client) -> dict:
    """
    Download both prompt versions from LangSmith Prompt Hub.
    Falls back to local templates if Hub is unavailable.
    """
    prompts = {}
    for name, fallback in [
        (PROMPT_V1_NAME, PROMPT_V1),
        (PROMPT_V2_NAME, PROMPT_V2),
    ]:
        try:
            prompts[name] = client.pull_prompt(name)
            print(f"  Pulled '{name}' from Hub")
        except Exception:
            prompts[name] = fallback
            print(f"  Using local fallback for '{name}'")
    return prompts


# ── 6. A/B routing — deterministic hash ─────────────────────────────────────
def get_prompt_version(request_id: str) -> str:
    """
    Route a request to prompt V1 or V2 based on the MD5 hash of request_id.

    even hash -> PROMPT_V1_NAME
    odd  hash -> PROMPT_V2_NAME

    DETERMINISTIC: same request_id always maps to the same version.
    """
    hash_int = int(hashlib.md5(request_id.encode()).hexdigest(), 16)
    return PROMPT_V1_NAME if hash_int % 2 == 0 else PROMPT_V2_NAME


# ── 7. Build vectorstore ─────────────────────────────────────────────────────
def build_vectorstore():
    """Load knowledge base, split, embed, and index with FAISS."""
    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base.txt"
    text = kb_path.read_text(encoding="utf-8")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    print(f"  Split into {len(chunks)} chunks")

    emb = OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    return FAISS.from_texts(chunks, emb)


# ── 8. Traced A/B query function ────────────────────────────────────────────
@traceable(name="ab-rag-query", tags=["ab-test", "step2"])
def ask_ab(retriever, llm, prompt, question: str, version: str) -> dict:
    """
    Run the RAG chain using the given prompt version.
    Returns a dict with question, answer, and version.
    """
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    answer = (prompt | llm | StrOutputParser()).invoke(
        {"context": context, "question": question}
    )
    return {"question": question, "answer": answer, "version": version}


# ── 9. Main ─────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Step 2: Prompt Hub A/B Routing")
    print("=" * 60)
    print(f"  Project : {os.environ.get('LANGCHAIN_PROJECT')}")
    print()

    # Tao LangSmith client
    client = Client(api_key=os.environ["LANGCHAIN_API_KEY"])

    # Push 2 prompt len Hub
    print("[1/4] Pushing prompts to LangSmith Prompt Hub...")
    push_prompts_to_hub(client)

    # Pull prompts tu Hub (co fallback local neu loi)
    print("\n[2/4] Pulling prompts from Hub...")
    prompts = pull_prompts_from_hub(client)

    # Build vectorstore va LLM
    print("\n[3/4] Building vectorstore and LLM...")
    vectorstore = build_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

    # Import danh sach 50 cau hoi tu step 1
    sys.path.insert(0, str(Path(__file__).parent))
    from importlib import import_module
    step1 = import_module("01_langsmith_rag_pipeline")
    questions = step1.SAMPLE_QUESTIONS

    # Loop 50 cau hoi qua A/B router
    print(f"\n[4/4] Running {len(questions)} questions through A/B router...\n")
    version_counts: Counter = Counter()

    for i, question in enumerate(questions):
        request_id  = f"req-{i:04d}"
        version_key = get_prompt_version(request_id)
        version_tag = "v1" if version_key == PROMPT_V1_NAME else "v2"
        prompt      = prompts[version_key]

        result = ask_ab(retriever, llm, prompt, question, version_tag)
        version_counts[version_tag] += 1
        print(f"[{i+1:02d}/50] [prompt-{version_tag}] {question[:55]}...")
        print(f"        {result['answer'][:100]}\n")

    # In routing summary
    print("=" * 60)
    print("  Routing Summary")
    print("=" * 60)
    for ver, count in sorted(version_counts.items()):
        print(f"  prompt-{ver}: {count} queries")
    total = sum(version_counts.values())
    print(f"  Total   : {total} queries")
    print()
    print(f"  {total} traces sent to LangSmith project '{os.environ['LANGCHAIN_PROJECT']}'")
    print("  Verify Prompt Hub: https://smith.langchain.com -> Prompt Hub")
    print("=" * 60)


if __name__ == "__main__":
    main()
