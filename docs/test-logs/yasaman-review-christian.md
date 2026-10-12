# Test Evidence Log — Independent Review of Christian's Tests

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Log entry ID:** YASAMAN-REVIEW-CHRISTIAN-01

> This log documents my independent execution and review of Christian's retrieval tests. All results are based on my own test runs. Information that I have not independently verified is explicitly marked as pending. I have not classified the observed failure as a confirmed software defect because the group has not yet formally agreed on the test oracle.

## 1. Identification

| Field | Value |
|---|---|
| Date | 2026-10-11 |
| Exact time / timezone | 09:15 (Swedish local time, CEST / UTC+02:00) |
| Tested by | Yasaman Vallaee |
| Risk area / technique | Retrieval relevance; independent reproduction of Golden Set tests |
| Test case IDs | G02, G03 (Christian's current test IDs) |
| Test file | `test_golden_set.py` |
| Test methods | `test_g02_retrieves_expense_report_deadline`; `test_g03_rejects_leave_amount_without_monetary_evidence` |
| Local branch | `review-christian` |
| Tracking branch | `origin/retrieval-relevance-golden-set-tests` |
| Commit hash | `43a61496a0e2ca50b6b43103a891aa8a4b57fbca` (verified with `git rev-parse HEAD`) |
| Suite | Extended suite (original tests + Christian's two retrieval tests) |
| Baseline reference | `baseline` tag, commit `b354c12` |

## 2. Environment and configuration

| Field | Value |
|---|---|
| Host operating system | Windows, version/build `10.0.26200.9457` (from `wsl --version`) |
| Guest/test operating system | Ubuntu 24.04.4 LTS (Noble Numbat), running under Windows Subsystem for Linux (WSL) |
| WSL version | `2.7.3.0` (WSL architecture generation not separately verified) |
| WSL Linux kernel | `6.6.114.1-1` |
| Python | 3.12.3 |
| pytest | 9.1.1 |
| Virtual environment | Project `.venv` activated |
| Python executable | `/home/yasam/miun/DV033G-testing/project/g6-pydantic-agentic-rag-testing/.venv/bin/python3` |
| Embedding backend | `HashingEmbeddingBackend` (from test implementation) |
| Embedding dimensions | 512 (from test implementation) |
| `min_relevance` | 0.20 (from test implementation) |
| `top_k` | 4 (from test implementation) |
| Model used by G02/G03 | None; retrieval-only tests |
| External API calls by G02/G03 | None; local in-memory store and hashing backend |
| External API calls by entire suite | Not independently network-monitored; original tests use simulated model behaviour |
| Additional package versions | `pluggy 1.6.0`, `pytest-cov 7.1.0` (as displayed in pytest plugin output) |

## 3. Test setup and oracle

### Shared synthetic documents

These are added in memory by `add_shared_documents()`; physical `.txt` files are not required for these tests.

`benefits.txt`:
> Eligible employees receive twelve weeks of paid parental leave after six months of employment.

`expenses.txt`:
> Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.

### G02 — Expense report deadline

- **Input:** `When must employees submit expense reports after business travel?`
- **Expected behaviour:** Retrieval marks evidence as sufficient.
- **Expected source:** `expenses.txt` ranked first.
- **Expected evidence:** A retrieved chunk contains `within thirty days`.
- **Pass conditions in the implemented test:** `result.enough_evidence` is true; `result.chunks[0].source == "expenses.txt"`; some returned chunk contains `within thirty days`.
- **Scope:** Retrieval only; this does not verify a generated answer.

### G03 — Unsupported monetary parental leave benefit

- **Input:** `What is the parental leave benefit amount in dollars?`
- **Expected behaviour in the implemented test:** Retrieval marks evidence as insufficient (`enough_evidence=False`).
- **Reason:** The shared documents state the *duration* of parental leave but do not specify a monetary parental leave benefit.
- **Pass condition in the implemented test:** `assertFalse(result.enough_evidence)`.
- **Scope:** Retrieval gate only; this does not demonstrate whether the final agent would answer or refuse.

**Oracle status:** These expectations are stated in the group's shared proposal sheet and in the test assertions. The **group-wide oracle strategy and defect-classification criteria are still pending formal approval**. The implementation's `enough_evidence` flag is determined by a similarity-score threshold, not a semantic entailment check.

## 4. Execution and actual results

### Run A — Christian's new tests only

```bash
python3 -m pytest test_golden_set.py -v
```

**Observed:** 2 tests collected; **1 passed, 1 failed**; 3.34 seconds.

| Test | Observed status | Evidence |
|---|---|---|
| G02 | PASS | `test_g02_retrieves_expense_report_deadline PASSED` |
| G03 | FAIL | `AssertionError: True is not false` at `test_golden_set.py:62` |

### Run B — Full original and extended test suite

```bash
python3 -m pytest test_typed_rag.py test_golden_set.py -v
```

**Observed:** 13 test methods collected; 12 passed, 1 failed, 5 subtests passed; 2.92 seconds.

- All 11 original test methods in `test_typed_rag.py` passed.
- G02 passed.
- G03 failed with the same assertion:

```text
>       self.assertFalse(result.enough_evidence)
E       AssertionError: True is not false

test_golden_set.py:62: AssertionError

FAILED test_golden_set.py::GoldenSetRetrievalTests::test_g03_rejects_leave_amount_without_monetary_evidence
1 failed, 12 passed, 5 subtests passed in 2.92s
```

**Actual G03 behaviour:** `result.enough_evidence` was `True` although the test expected `False`.

**Similarity score / top-ranked source:** The exact similarity score and top-ranked source for G03 were not captured in my terminal output.

However, I independently verified that retrieve_evidence() returned enough_evidence=True, while the test expected False.

A separate measurement is required to document the exact similarity score and top-ranked source.

**Overall status:** FAIL (one test fails). The original test suite remains green.

**Evidence location:** Terminal output copied into the conversation; no permanent terminal-output file has yet been saved. To preserve a fresh run in the repository, rerun with `-v` and redirect or tee output to a dated file after choosing the group's evidence storage convention.

**Independent reproduction:** I reproduced the failure locally on 2026-10-11 at approximately 09:15 CEST. Other members' own execution details are not established by this record.

## 5. Findings and interpretation

**Expected vs actual:** G03 expected `enough_evidence=False`; the retrieval function returned `True`.

**Possible explanation (hypothesis):** The retrieval gate treats a sufficiently high lexical similarity score as sufficient evidence. A question can share words with a document about parental leave without that document containing the requested monetary amount. This is consistent with the implementation's threshold-based design; the captured run alone does not establish the exact score.

**Classification:** Unclassified reproduced test failure, pending agreement on the test oracle. It may be treated as a defect against an accepted semantic-evidence requirement or as a known design limitation of the existing threshold gate.

**Important limitation:** These tests call `retrieve_evidence()` and do not verify final generated answers or citations. A green original suite does not establish that all application behaviour is correct.

**Changes to SUT:** None reported. The working tree was clean before execution (`git status`).

## 6. Follow-up

| Field | Value |
|---|---|
| Action required | Agree on oracle; classify G03; decide how to preserve/report the known failing test; align case IDs with shared sheet |
| Test owner | Christian |
| Independent reviewer | Yasaman |
| Related branch | `retrieval-relevance-golden-set-tests` |
| PR number / URL | https://github.com/yasva/g6-pydantic-agentic-rag-testing/pull/2 |
| Review status | Open — no merge or approval recorded |
| Group review date | Pending |

### Verification still needed

- [x] Add exact commit hash using `git rev-parse HEAD`.
- [x] Verify that G02/G03 IDs match Christian's current proposals.
- [ ] Record formal group approval of the test cases, if required.
- [ ] Decide whether to retain G03 as a failing test or mark it as an expected failure, with a written rationale.
- [ ] Save permanent raw terminal output if required by the group's evidence policy.
- [x] Record the reviewed PR URL/number when available.

**Summary:** I independently ran Christian's retrieval tests and the full extended suite. G02 passed, G03 failed reproducibly, and all 11 original test methods passed. The failure is documented without prematurely calling it a confirmed defect.
