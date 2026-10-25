# Test Evidence Log — Group 6

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Tested by:** Marjan Motafeghizenoz

## 1. Purpose and Scope

This log records the execution and findings of G05, G06 and G07, focusing on insufficient evidence and refusal behaviour.

G05 checks refusal through the retrieval preflight gate. G06 and G07 use controlled model responses to check whether the application rejects unsupported claims accompanied by authentic quotations.

These tests do not evaluate a live language model or measure how frequently it generates unsupported answers.

## Test setup — G05, G06 and G07

| Field | Value |
|---|---|
| Test oracle / reference | Shared synthetic documents provide the reference facts; assertions in `test_golden_set.py` define the expected refusal behaviour. |
| Test case IDs | G05, G06 and G07 |
| Shared documents | Synthetic `benefits.txt` and `expenses.txt`; exact contents are reproduced below. |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.20 |
| `top_k` | 3 |
| Model configuration | G05 checks refusal at the retrieval preflight gate without invoking a model. G06 and G07 use PydanticAI’s `TestModel` with controlled responses. No live language model is used. |
| Baseline tag / commit | `baseline` / `b354c12` |
| Pass conditions | All three tests require `answered=False` and empty citations. G05 additionally requires the exact `REFUSAL_TEXT`. |
---

# Test Execution Record — MARJAN-GOLDEN-SET-01 (G05 and G06)

## 1. Identification

| Field | Value |
|---|---|
| Log entry ID | MARJAN-GOLDEN-SET-01 |
| Tested by | Marjan Motafeghi |
| Risk area / testing technique | Insufficient evidence and refusal; retrieval preflight and validation of controlled unsupported answers |
| Test case IDs | G05 and G06 |
| Test file | `test_golden_set.py` |
| Test methods | `GoldenSetRefusalTests.test_g05_refuses_unrelated_question`; `GoldenSetRefusalTests.test_g06_insufficient_annual_allowance_evidence` |
| Reported working branch | `test/golden-set-refusal-marjan`; the exact checkout was not captured in the execution record. |
| Suite | Extended Golden Set tests; this recorded run included G05 and G06, before G07 was added. |

## 2. Environment and Configuration

| Field | Value |
|---|---|
| Operating system | macOS |
| Test framework | Python `unittest` |
| Virtual environment | Project `.venv` |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.20 |
| `top_k` | 3 |
| Model configuration | G05: no model invoked when the retrieval preflight refuses. G06: `TestModel(call_tools=["retrieve"])`. |
| External model requests | Disabled using `models.ALLOW_MODEL_REQUESTS = False`. |

## 3. Test Setup and Oracle

**Shared test documents**

Each test creates two in-memory documents:

- `benefits.txt`: “Eligible employees receive twelve weeks of paid parental leave after six months of employment.”
- `expenses.txt`: “Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.”

**Questions**

- **G05:** “Who won the 1978 World Cup?”
- **G06:** “What is the annual meal allowance?”

**Controlled model output — G06**

G06 supplies a deliberately unsupported response through `TestModel`:

> The annual meal allowance is 70 dollars.

The response cites the authentic quotation:

> The daily meal allowance is 70 dollars.

**Expected behaviour and evidence**

- **G05:** Refuse because neither document contains evidence answering the question.
- **G06:** Reject the simulated annual claim because `expenses.txt` specifies a daily allowance, not an annual amount. The quotation is authentic but does not support the claim.

**Test oracle**

The synthetic documents provide the reference facts, and the test assertions define the expected refusal behaviour. These expectations are used to identify findings; a failed assertion alone does not establish a confirmed software defect.

**Measurable pass conditions**

- **G05:** `answer.answered is False`, `answer.citations == []`, and `answer.text == REFUSAL_TEXT`.
- **G06:** `answer.answered is False` and `answer.citations == []` after the controlled response is supplied.

**Scope**

- **G05:** Checks the final refusal returned by `answer_question()` through the retrieval preflight gate.
- **G06:** Checks the final output of `answer_question()` after a simulated agent response with an authentic citation. It does not evaluate the answer-generation behaviour of a live language model.

## 4. Execution and actual results

**Exact command(s):**

```bash
python -m unittest test_golden_set.GoldenSetRefusalTests -v
```

**Result summary (number passed / failed / xfailed / xpassed / errors / subtests):**

2 tests run: **1 passed, 1 failed**, 0 errors; `Ran 2 tests in 0.014s`. No xfail/xpass status reported.

**Actual output / behaviour (include scores, top-ranked source and `enough_evidence` where relevant):**

```text
test_g05_refuses_unrelated_question (test_golden_set.GoldenSetRefusalTests.test_g05_refuses_unrelated_question) ... ok
test_g06_insufficient_annual_allowance_evidence (test_golden_set.GoldenSetRefusalTests.test_g06_insufficient_annual_allowance_evidence) ... FAIL

FAIL: test_g06_insufficient_annual_allowance_evidence
AssertionError: True is not false : G06: The system must refuse an unsupported annual allowance.

Ran 2 tests in 0.014s
FAILED (failures=1)
```

G05 refused as expected. In G06, the assertion received `answer.answered=True` instead of the expected `False`. The run did not capture the exact retrieval score or ranked sources; do not infer them from this output.

**Status:** **FAIL** overall (G05 PASS; G06 FAIL).

**Evidence location (terminal output file, screenshot, CI URL, commit or log path):**

Terminal output was shared in the project discussion. A permanent raw output file or CI link has not yet been recorded.

**Reproduced by another group member? If yes, who and when:**

Not yet independently reproduced.

## 5. Findings and interpretation

**Expected vs actual difference:**

G06 expected the system to reject an unsupported *annual* amount. It instead accepted the simulated answer, setting `answered=True`. G05 behaved as expected.

**Possible cause (hypothesis, not yet verified):**

The citation checker validates whether a quoted span appears in a stored chunk, but may not verify that the quotation logically supports the complete claim. A genuine quote about a daily allowance can accompany an unsupported annual claim.

**Classification:** **Unclassified reproduced test failure**, pending agreement on the oracle. Not yet a group-confirmed defect.

**Oracle-based rationale for classification:**

The test's refusal expectation is explicit, and the observed failure is real. However, the team has not formally approved whether semantic claim support is a requirement of the existing guardrail, so final defect versus design-limitation classification is pending.

**Known limitations / confounding factors:**

G06 uses a deliberately configured `TestModel`, not a real LLM. This demonstrates the validation path's response to an unsupported output, not the frequency of hallucinations by an actual model. No independent rerun, exact commit hash, dependency versions, or permanent terminal log is yet available.

**Changes to SUT (none / temporary and reverted / other):**

No production `agent.py` or `rag.py` changes reported; changes were made to Golden Set test code.

## 6. Follow-up

| Field | Value |
|---|---|
| Action required | Agree on oracle and classification; independently reproduce G06; capture exact environment, commit, and permanent test output |
| Responsible person | Marjan (test author); group/reviewer for approval |
| Status (open / under review / resolved) | Open — review pending |
| Date reviewed by group | Pending |

**Additional notes:** This execution occurred before G07 was added to the test class. Therefore the command collected only G05 and G06.

---

# Test Execution Record — MARJAN-GOLDEN-SET-02 (G07)

## 1. Identification

| Field | Value |
|---|---|
| Log entry ID | MARJAN-GOLDEN-SET-02 |

| Tested by | Marjan Motafeghi |
| Risk area / testing technique | Insufficient evidence and refusal; simulated unsupported-answer validation |
| Test case ID(s) | G07 (Marjan's current ID; similar question appears as Christian's G03, but tests a different layer) |
| Test method(s) / file | `test_golden_set.py`: `GoldenSetRefusalTests.test_g07_refuses_unsupported_parental_leave_amount` |
| Branch | `test/golden-set-refusal-marjan` (working branch reported; exact checkout at execution not independently captured) |
| Commit hash (`git rev-parse HEAD`) | Pending verification |
| Baseline or extended suite | Extended Golden Set; G07 method executed individually |

## 2. Environment and configuration

| Field | Value |
|---|---|
| Operating system | macOS (MacBook Air; exact version not captured) |
| pytest version | Not applicable to recorded command (`unittest` was used) |
| Virtual environment | Project `.venv` activated |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.20 |
| `top_k` | 3 |
| Model / TestModel / FunctionModel / none | PydanticAI `TestModel(call_tools=["retrieve"])` |
| External API calls (yes/no) | No external model calls allowed (`models.ALLOW_MODEL_REQUESTS = False` during test); network traffic not independently monitored |

## 3. Test setup and oracle

**Shared test documents / synthetic data (exact content or file reference):**

- `benefits.txt`: `Eligible employees receive twelve weeks of paid parental leave after six months of employment.`
- `expenses.txt`: `Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.`

Both documents are added to an in-memory vector store by the test setup.

**Original question / input:**

`What is the parental leave benefit amount in dollars?`

**Paraphrased question / transformed input (if applicable):**

Not a paraphrase test. A simulated model output is injected: `The parental leave benefit is 5000 dollars.`

**Expected behaviour (answer / refuse / other):**

Refuse the unsupported monetary amount because the document describes the *duration* of paid leave, not the benefit amount in dollars.

**Expected source, evidence, citation or refusal reason:**

`benefits.txt` contains `twelve weeks of paid parental leave`. This is a genuine quote but does not justify the simulated claim of 5000 dollars.

**Test oracle (approved case, documented rule, metamorphic relation, etc.):**

Provisional Golden Set refusal expectation and explicit assertions. Group-wide oracle approval and defect classification are pending.

**Measurable pass condition(s):**

`answer.answered is False` and `answer.citations == []` after the simulated unsupported output.

**Scope of assertion (retrieval / agent output / citation / other):**

Final `answer_question()` output and citation validation using a simulated model response. This does not test a real LLM's generated answer.

## 4. Execution and Actual Results

### Run 1 — G05 and G06

This run took place before G07 was added to the test class, so the command executed only G05 and G06.

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

**Result:** 2 tests run; 1 passed, 1 failed, 0 errors.

G05 returned the expected refusal. G06 accepted the simulated annual allowance of 70 dollars, returning `answer.answered=True` instead of the expected `False`.

### Run 2 — G07

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

**Result:** 1 test run; 0 passed, 1 failed, 0 errors.

G07 accepted the simulated parental leave benefit of 5000 dollars, returning `answer.answered=True` instead of the expected `False`. The cited document describes leave duration but contains no monetary benefit amount.

### Overall Results — G05, G06 and G07

The table summarises the two recorded runs above, rather than a separate execution of all three tests together.

| Test | Result | Observation |
|---|---|---|
| G05 | PASS | The system refused the unrelated question. |
| G06 | FAIL | The system accepted the simulated unsupported annual allowance. |
| G07 | FAIL | The system accepted the simulated unsupported parental leave amount. |

**Evidence:** Terminal output shared in the project discussion.

Exact retrieval scores and ranked source lists were not captured in these runs.

## 5. Findings and Interpretation

### Expected and Observed Behaviour

G05 passed: the application refused the unrelated question as expected.

G06 failed: the application accepted a simulated annual meal allowance of 70 dollars, although the document specifies only a daily allowance.

G07 failed: the application accepted a simulated parental leave benefit of 5000 dollars, although the document specifies leave duration but no monetary amount. The response returned `answer.answered=True`, while the test expected `False`.

### Interpretation

G06 and G07 used authentic quotations alongside unsupported claims. The findings indicate a limitation in answer validation: quotation authenticity does not establish that the quoted text supports the claim.

These responses were supplied through `TestModel`. The results do not demonstrate that a live language model generated the incorrect claims or establish real-model hallucination rates.

### Classification

The failures are documented findings, not confirmed software defects. Classification as a defect depends on whether claim-level semantic validation is an intended application requirement.

### Distinction Between G03 and G07

Both tests ask about the missing parental leave amount, but they check different stages. G03 checks `retrieve_evidence()` and its `enough_evidence` flag. G07 checks final-answer validation through `answer_question()`.

### Changes to the System Under Test

No production changes to `agent.py` or `rag.py` were reported; changes concerned test code only.

## 6. Follow-up

- Review whether claim-level semantic validation is an intended application requirement.
- Use that requirement to distinguish software defects from design limitations.