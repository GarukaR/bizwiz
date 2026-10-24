"""Ask the real Claude API one question and check the citations. Costs about 3 US cents.

Run from backend/ with the database up and ANTHROPIC_API_KEY in ../.env:

    uv run python scripts/smoke.py "What is the fuel levy?"
"""

import os
import sys

from bizwiz.index.postgres import PostgresIndex
from bizwiz.pipeline import ask
from bizwiz.wiring import build_answerer, build_app

question = sys.argv[1] if len(sys.argv) > 1 else "What is the fuel levy?"
build_app()  # loads .env and indexes the corpus
os.environ["ANSWERER"] = "claude"
index = PostgresIndex(
    os.environ.get("DATABASE_URL", "postgresql://bizwiz:bizwiz@localhost:5442/bizwiz")
)
answer = ask(question, index=index, answerer=build_answerer())

print(f"Q: {question}\nA: {answer.text}\n")
ok = bool(answer.citations)
for i, c in enumerate(answer.citations, 1):
    found = c.quoted_text in index.get(c.passage_id).text
    ok = ok and found
    print(f"[{i}] {c.doc_title} ({c.passage_id}) quote found in source: {found}")
    print(f"    {c.quoted_text!r}")
print("\nSMOKE OK" if ok else "\nSMOKE FAILED: no citations, or a quote is not in its source")
sys.exit(0 if ok else 1)
