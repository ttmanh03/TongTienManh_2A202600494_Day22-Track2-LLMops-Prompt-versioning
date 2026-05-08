"""
run_all.py — Chay toan bo lab Day 22 theo thu tu
================================================
Usage:
    python run_all.py           # chay tat ca 4 steps
    python run_all.py --step 1  # chi chay step 1
    python run_all.py --step 3  # chi chay step 3

Evidence collection:
    python run_all.py --step 2 | tee evidence/02_ab_routing_log.txt
    python run_all.py --step 4 | tee evidence/04_pii_demo_log.txt
"""

import sys
import os
import argparse
import shutil
from pathlib import Path

# Them pseudocode/ vao sys.path de import cac module
ROOT = Path(__file__).parent
PSEUDO = ROOT / "pseudocode"
sys.path.insert(0, str(PSEUDO))


def run_step1():
    print("\n" + "#" * 60)
    print("  STEP 1 — LangSmith RAG Pipeline")
    print("#" * 60)
    import importlib
    step1 = importlib.import_module("01_langsmith_rag_pipeline")
    step1.main()


def run_step2():
    print("\n" + "#" * 60)
    print("  STEP 2 — Prompt Hub & A/B Routing")
    print("#" * 60)
    import importlib
    step2 = importlib.import_module("02_prompt_hub_ab_routing")
    step2.main()


def run_step3():
    print("\n" + "#" * 60)
    print("  STEP 3 — RAGAS Evaluation (~20-30 min)")
    print("#" * 60)
    import importlib
    step3 = importlib.import_module("03_ragas_evaluation")
    step3.main()

    # Tu dong copy ragas_report.json vao evidence/
    src = ROOT / "data" / "ragas_report.json"
    dst = ROOT / "evidence" / "03_ragas_report.json"
    if src.exists():
        dst.parent.mkdir(exist_ok=True)
        shutil.copy(src, dst)
        print(f"\n  Copied {src.name} -> evidence/03_ragas_report.json")


def run_step4():
    print("\n" + "#" * 60)
    print("  STEP 4 — Guardrails AI Validators")
    print("#" * 60)
    import importlib
    step4 = importlib.import_module("04_guardrails_validator")
    step4.main()


STEPS = {
    1: run_step1,
    2: run_step2,
    3: run_step3,
    4: run_step4,
}


def main():
    parser = argparse.ArgumentParser(description="Run Day 22 lab steps")
    parser.add_argument(
        "--step", type=int, choices=[1, 2, 3, 4],
        help="Chay mot step cu the (1-4). Mac dinh: chay tat ca."
    )
    args = parser.parse_args()

    # Tao thu muc evidence neu chua co
    (ROOT / "evidence").mkdir(exist_ok=True)

    if args.step:
        STEPS[args.step]()
    else:
        print("Running all 4 steps...")
        print("NOTE: Step 3 (RAGAS) takes ~20-30 minutes.\n")
        for step_num, step_fn in STEPS.items():
            step_fn()

    print("\n" + "=" * 60)
    print("  Done! Check evidence/ folder for saved outputs.")
    print("  For screenshots, open https://smith.langchain.com")
    print("=" * 60)


if __name__ == "__main__":
    main()
