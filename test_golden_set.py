import asyncio
import unittest

from agent import RagDependencies, retrieve_evidence
from rag import HashingEmbeddingBackend, InMemoryVectorStore

# Golden Set Retrieval Tests
class GoldenSetRetrievalTests(unittest.TestCase):
    """Retrieval checks for the agreed shared test documents."""
    def run_async(self, awaitable):
        return asyncio.run(awaitable)
    def make_store(self):
        return InMemoryVectorStore(HashingEmbeddingBackend(dimensions=512))
    def add_shared_documents(self, store):
        """Index the same documents used to define the Golden Set cases."""
        self.run_async(
            store.add_document(
                "benefits.txt",
                "Eligible employees receive twelve weeks of paid parental leave "
                "after six months of employment.",
            )
        )
        self.run_async(
            store.add_document(
                "expenses.txt",
                "Employees must submit expense reports within thirty days after "
                "business travel. The daily meal allowance is 70 dollars.",
            )
        )
    def test_g02_retrieves_expense_report_deadline(self):
        """G02: retrieve sufficient evidence for the expense-report question."""
        store = self.make_store()
        self.add_shared_documents(store)
        deps = RagDependencies(store=store, min_relevance=0.2, top_k=4)

        result = self.run_async(
            retrieve_evidence(
                deps,
                "When must employees submit expense reports after business travel?",
            )
        )
        self.assertTrue(result.enough_evidence)
        self.assertEqual("expenses.txt", result.chunks[0].source)
        self.assertTrue(
            any(
                "within thirty days" in chunk.text.lower()
                for chunk in result.chunks
            )
        )
    def test_g03_rejects_leave_amount_without_monetary_evidence(self):
        """G03: a leave duration must not count as evidence of a dollar amount."""
        store = self.make_store()
        self.add_shared_documents(store)
        deps = RagDependencies(store=store, min_relevance=0.2, top_k=4)

        result = self.run_async(
            retrieve_evidence(
                deps,
                "What is the parental leave benefit amount in dollars?",
            )
        )
        self.assertFalse(result.enough_evidence)


# SHARED TEST DOCUMENTS
#
# Use these same synthetic documents when proposing initial cases:
#
# benefits.txt:
# "Eligible employees receive twelve weeks of paid parental leave after six
# months of employment."
#
# expenses.txt:
# "Employees must submit expense reports within thirty days after business
# travel. The daily meal allowance is 70 dollars."
#
# If a proposed case needs additional or conflicting information, describe the
# proposed change in the Word proposal sheet. The group must approve changes so
# all final tests use the same agreed test documents.



# WORK SEQUENCE
#
# TODO 1: Each member drafts 2–3 cases in their assigned risk area in the shared
#         Word proposal sheet.
# TODO 2: Review the expected evidence, answer/refusal decision, and pass
#         condition together.
# TODO 3: Remove duplicates and check that the cases cover all five planned
#         risks: incorrect/irrelevant retrieval, unsupported answers,
#         incorrect citations, answering without enough evidence, and
#         inconsistent behaviour for equivalent questions.
# TODO 4: Agree on and record the final cases and shared test documents.
# TODO 5: Implement only the approved automated tests in THIS file:
#         test_golden_set.py.
# TODO 6: Follow the deterministic test patterns in test_typed_rag.py and avoid
#         external API calls in automated tests where possible.
# TODO 7: Run the new tests and then the complete suite. Save the command,
#         environment, and results.
# TODO 8: Compare baseline and extended results in the same environment.
#         Record findings, blockers, limitations, and remaining work.

import asyncio
import unittest

from agent import RagDependencies, retrieve_evidence
from rag import HashingEmbeddingBackend, InMemoryVectorStore


class MetamorphicTests(unittest.TestCase):
    def test_m01_paraphrase_invariance(self):
        store = InMemoryVectorStore(HashingEmbeddingBackend(dimensions=512))

        asyncio.run(
            store.add_document(
                "benefits.txt",
                "Eligible employees receive twelve weeks of paid parental leave "
                "after six months of employment.",
            )
        )

        asyncio.run(
            store.add_document(
                "expenses.txt",
                "Employees must submit expense reports within thirty days "
                "after business travel. The daily meal allowance is 70 dollars.",
            )
        )

        deps = RagDependencies(store=store, min_relevance=0.2, top_k=4)

        original = asyncio.run(
            retrieve_evidence(
                deps,
                "How many weeks of paid parental leave do eligible employees receive?",
            )
        )

        paraphrase = asyncio.run(
            retrieve_evidence(
                deps,
                "What is the duration of paid parental leave for eligible employees?",
            )
        )

        for result in (original, paraphrase):
            self.assertTrue(result.enough_evidence)
            self.assertTrue(result.chunks)
            self.assertEqual("benefits.txt", result.chunks[0].source)
            self.assertIn("twelve weeks of paid parental leave", result.chunks[0].text)

    def test_m02_expense_report_paraphrase(self):
        store = InMemoryVectorStore(HashingEmbeddingBackend(dimensions=512))

        asyncio.run(
            store.add_document(
                "benefits.txt",
                "Eligible employees receive twelve weeks of paid parental leave "
                "after six months of employment.",
            )
        )

        asyncio.run(
            store.add_document(
                "expenses.txt",
                "Employees must submit expense reports within thirty days "
                "after business travel. The daily meal allowance is 70 dollars.",
            )
        )

        deps = RagDependencies(store=store, min_relevance=0.2, top_k=4)

        original = asyncio.run(
            retrieve_evidence(
                deps,
                "When must employees submit expense reports after business travel?",
            )
        )

        paraphrase = asyncio.run(
            retrieve_evidence(
                deps,
                "How soon after business travel are expense reports due?",
            )
        )

        for result in (original, paraphrase):
            self.assertTrue(result.enough_evidence)
            self.assertTrue(result.chunks)
            self.assertEqual("expenses.txt", result.chunks[0].source)
            self.assertIn("within thirty days", result.chunks[0].text)

    def test_m04_meal_allowance_paraphrase(self):
        """M04: Paraphrasing a monetary amount question preserves evidence."""

        store = InMemoryVectorStore(HashingEmbeddingBackend(dimensions=512))

        asyncio.run(
            store.add_document(
                "benefits.txt",
                "Eligible employees receive twelve weeks of paid parental leave "
                "after six months of employment.",
            )
        )

        asyncio.run(
            store.add_document(
                "expenses.txt",
                "Employees must submit expense reports within thirty days "
                "after business travel. The daily meal allowance is 70 dollars.",
            )
        )

        deps = RagDependencies(store=store, min_relevance=0.2, top_k=4)

        original = asyncio.run(
            retrieve_evidence(
                deps,
                "What is the daily meal allowance?",
            )
        )

        paraphrase = asyncio.run(
            retrieve_evidence(
                deps,
                "How much is the meal allowance per day?",
            )
        )

        for result in (original, paraphrase):
            self.assertTrue(result.enough_evidence)
            self.assertTrue(result.chunks)
            self.assertEqual("expenses.txt", result.chunks[0].source)
            self.assertIn(
                "The daily meal allowance is 70 dollars.",
                result.chunks[0].text,
            )
            