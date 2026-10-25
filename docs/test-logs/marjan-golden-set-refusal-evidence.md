# Test Evidence Log — Group 6

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Tested by:** Marjan Motafeghizenoz

## Purpose and Scope

This log records G05, G06 and G07. The tests check whether the application refuses questions or answers that lack supporting evidence.

G05 checks refusal before a model is called. G06 and G07 use `TestModel` to provide unsupported answers with real quotations.

The tests do not evaluate a live language model or measure how often it produces incorrect answers.

Marjan’s original runs, the later group run and the Codex run are recorded separately.

## 1. Identification

| Field | Value |
|---|---|
| Test cases | G05, G06 and G07 |
| Test file | `test_golden_set.py` |
| G05 method | `GoldenSetRefusalTests.test_g05_refuses_unrelated_question` |
| G06 method | `GoldenSetRefusalTests.test_g06_insufficient_annual_allowance_evidence` |
| G07 method | `GoldenSetRefusalTests.test_g07_refuses_unsupported_parental_leave_amount` |
| Reported branch | `test/golden-set-refusal-marjan`; the exact checkout was not captured in the original run record. |
| Suite | Extended Golden Set tests |
| Run records | MARJAN-GOLDEN-SET-01: G05 and G06; MARJAN-GOLDEN-SET-02: G07 |
| Baseline tag / commit | `baseline` / `b354c12` |

## 2. Environment and Configuration

These settings apply to Marjan’s three tests.

| Field | Value |
|---|---|
| Operating system | macOS |
| Test framework | Python `unittest` |
| Virtual environment | Project `.venv` |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.20 |
| `top_k` | 3 |
| G05 model | None; the retrieval gate refuses before a model is called |
| G06 and G07 model | `TestModel(call_tools=["retrieve"])` |
| External model requests | Disabled with `models.ALLOW_MODEL_REQUESTS = False` |

Network traffic was not separately monitored during the original runs.

## 3. Test Setup and Oracle

### Shared Test Documents

Each test adds two documents to an in-memory store.

**benefits.txt**

> Eligible employees receive twelve weeks of paid parental leave after six months of employment.

**expenses.txt**

> Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.

The documents give a leave duration and a daily meal allowance. They do not give a parental leave payment amount or an annual meal allowance.

### Questions and Expected Behaviour

| Test | Question | Expected behaviour |
|---|---|---|
| G05 | Who won the 1978 World Cup? | Refuse because neither document answers the question. |
| G06 | What is the annual meal allowance? | Reject the unsupported annual amount. |
| G07 | What is the parental leave benefit amount in dollars? | Reject the unsupported payment amount. |

### Controlled Model Responses

These are not paraphrase tests. G06 and G07 use scripted answers.

| Test | Simulated answer | Real quotation used as a citation |
|---|---|---|
| G06 | The annual meal allowance is 70 dollars. | The daily meal allowance is 70 dollars. |
| G07 | The parental leave benefit is 5000 dollars. | twelve weeks of paid parental leave |

The G06 quotation supports a daily amount, not an annual amount. The G07 quotation supports leave duration, not a payment of 5000 dollars.

### Test Oracle

The synthetic documents provide the known facts. The test assertions define the expected refusal behaviour.

A failed test is recorded as a finding. It is not automatically treated as a confirmed software defect.

### Pass Conditions

| Test | Required result |
|---|---|
| G05 | `answer.answered is False`, `answer.citations == []`, and `answer.text == REFUSAL_TEXT` |
| G06 | `answer.answered is False` and `answer.citations == []` |
| G07 | `answer.answered is False` and `answer.citations == []` |

### Scope

G05 checks the refusal returned by `answer_question()` through the retrieval gate.

G06 and G07 check the final result of `answer_question()` after a controlled model response. They test application validation, not live-model answer quality.

## 4. Execution and Actual Results

### Run 1 — G05 and G06

**Log entry:** MARJAN-GOLDEN-SET-01

This run happened before G07 was added, so the command ran only G05 and G06.

**Command**

```bash
python -m unittest test_golden_set.GoldenSetRefusalTests -v
```

**Recorded output**

```text
test_g05_refuses_unrelated_question (test_golden_set.GoldenSetRefusalTests.test_g05_refuses_unrelated_question) ... ok
test_g06_insufficient_annual_allowance_evidence (test_golden_set.GoldenSetRefusalTests.test_g06_insufficient_annual_allowance_evidence) ... FAIL

FAIL: test_g06_insufficient_annual_allowance_evidence
AssertionError: True is not false : G06: The system must refuse an unsupported annual allowance.

Ran 2 tests in 0.014s
FAILED (failures=1)
```

**Result:** 1 passed, 1 failed, 0 errors.

G05 refused as expected. G06 accepted the simulated annual amount and returned `answer.answered=True` instead of `False`.

### Run 2 — G07

**Log entry:** MARJAN-GOLDEN-SET-02

G07 was run separately.

**Command**

```bash
python -m unittest test_golden_set.GoldenSetRefusalTests.test_g07_refuses_unsupported_parental_leave_amount -v
```

**Recorded output**

```text
test_g07_refuses_unsupported_parental_leave_amount (test_golden_set.GoldenSetRefusalTests.test_g07_refuses_unsupported_parental_leave_amount) ... FAIL

FAIL: test_g07_refuses_unsupported_parental_leave_amount
AssertionError: True is not false : G07: The system must refuse an unsupported monetary amount.

Ran 1 test in 0.014s
FAILED (failures=1)
```

**Result:** 0 passed, 1 failed, 0 errors.

G07 accepted the simulated payment of 5000 dollars and returned `answer.answered=True` instead of `False`.

### Overall Results

This table combines the results of the two separate runs.

| Test | Result | Observation |
|---|---|---|
| G05 | PASS | The application refused the unrelated question. |
| G06 | FAIL | The application accepted the unsupported annual allowance. |
| G07 | FAIL | The application accepted the unsupported parental leave payment. |

### Evidence Location

The terminal output was shared in the project discussion. No separate raw-output file or CI link was recorded for these original runs.

Retrieval scores and ranked sources were not saved. G07’s `enough_evidence` value was not printed separately.

### Later Verification — Group Run

The repository contains these saved logs:

- `docs/test-logs/coverage-baseline-2026-10-15.txt`
- `docs/test-logs/coverage-extended-2026-10-15.txt`

| Reference | Revision |
|---|---|
| Tested application revision | `fb894b8fba719cdfa5bd04cb4481cdc2938f25ef` |
| Commit containing the execution evidence | `bd6f266` |

The combined group run recorded **17 passed and 4 failed out of 21 tests**.

G03, G06, G07 and M04 failed. G05 passed.

### Later Verification — Codex Run

Codex separately ran the original and extended suites during the repository review. This was an automated check, not a run by another group member.

**Reviewed revision**

`25ed55244afa2179e06e169be3d5f1f61b8e31dd`

The review found no changes in `agent.py`, `rag.py`, `test_typed_rag.py` or `test_golden_set.py` between this revision and `fb894b8`.

| Environment | Version |
|---|---|
| Operating system | Linux |
| Python | 3.12.14 |
| pytest | 9.1.1 |
| pytest-cov | 7.1.0 |

**Command**

```bash
python -m pytest test_typed_rag.py test_golden_set.py --cov=agent --cov=rag --cov-branch --cov-report=term --tb=short
```

**Result**

```text
4 failed, 17 passed in 41.30s
```

The same four cases failed: G03, G06, G07 and M04.

### Comparison of Results

| Test | Marjan’s original runs | Group run | Codex run |
|---|---|---|---|
| G05 | PASS | PASS | PASS |
| G06 | FAIL | FAIL | FAIL |
| G07 | FAIL | FAIL | FAIL |

The later runs reproduced the outcomes. Their environment and revision details do not describe Marjan’s earlier runs.

## 5. Findings and Interpretation

### Expected vs Actual Behaviour

G05 worked as expected.

G06 and G07 accepted unsupported monetary claims with real quotations. G06 used a daily allowance quotation to support an annual claim. G07 used a leave-duration quotation to support a payment claim.

### Technical Explanation

Code review showed that citation validation checks whether the source and chunk exist and whether the quotation appears in that chunk. It normalises whitespace and letter case before comparing the text.

It does not check whether the quotation supports the meaning of the answer’s claim.

A real quotation can therefore pass validation while accompanying an unsupported answer.

### Classification

The group report records these as **F02 / G06** and **F03 / G07**.

They are documented findings, not confirmed software defects. Defect classification depends on whether checking claim-level support is an intended application requirement.

Reproducing a failure confirms the observed behaviour. It does not by itself approve the oracle or establish a software defect.

### Known Limitations

The tests use two short synthetic documents and local hashing embeddings.

G06 and G07 use `TestModel` responses. They do not show that a live model generated these claims or measure how often such errors occur.

The original runs did not capture exact retrieval scores or ranked sources.

### Changes to SUT

No production changes to `agent.py` or `rag.py` were reported. Changes concerned Golden Set test code.

### Additional Notes — G03 and G07

G03 and G07 ask about the same missing parental leave amount but test different stages.

G03 checks `retrieve_evidence()` and its `enough_evidence` flag. G07 checks the final answer through `answer_question()` after a controlled model response.

## 6. Follow-up

- Review whether claim-level support is an intended application requirement.
- Use that requirement to distinguish software defects from design limitations.