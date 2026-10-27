"""Print retrieval scores for the questions behind findings F01 (G03) and F04 (M04).

Run from the repository root at the tested revision, with no OPENAI_API_KEY set:

    env -u OPENAI_API_KEY python score_trace.py | tee docs/test-logs/score-trace-YYYY-MM-DD.txt

Configuration matches the tests: hashing backend, 512 dimensions,
min_relevance=0.2, top_k=4.
"""

import asyncio
import os
import platform
import subprocess

from agent import RagDependencies, retrieve_evidence
from rag import HashingEmbeddingBackend, InMemoryVectorStore

DOCUMENTS = [
    (
        "benefits.txt",
        "Eligible employees receive twelve weeks of paid parental leave "
        "after six months of employment.",
    ),
    (
        "expenses.txt",
        "Employees must submit expense reports within thirty days after "
        "business travel. The daily meal allowance is 70 dollars.",
    ),
]

QUESTIONS = [
    ("G03/G07", "What is the parental leave benefit amount in dollars?"),
    ("M04 original", "What is the daily meal allowance?"),
    ("M04 paraphrase", "How much is the meal allowance per day?"),
]


async def main():
    store = InMemoryVectorStore(HashingEmbeddingBackend(dimensions=512))
    for source, text in DOCUMENTS:
        await store.add_document(source, text)
    deps = RagDependencies(store=store, min_relevance=0.2, top_k=4)

    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    print(
        f"commit={commit} python={platform.python_version()} os={platform.platform()}"
    )
    print(f"OPENAI_API_KEY set: {bool(os.environ.get('OPENAI_API_KEY'))}")
    print(f"chunks: {[(c.source, c.chunk_id) for c in store.chunks]}")
    for case_id, question in QUESTIONS:
        result = await retrieve_evidence(deps, question)
        ranking = ", ".join(f"{c.source}={c.score:.4f}" for c in result.chunks)
        print(
            f"{case_id:15} enough_evidence={result.enough_evidence!s:5} {ranking} :: {question}"
        )


asyncio.run(main())
