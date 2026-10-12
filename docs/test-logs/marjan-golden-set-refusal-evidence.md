# Test Evidence Log — Group 6

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Purpose:** Record reproducible, independently verifiable evidence for the baseline and extended test suite.

> **Instructions:** Each group member records observed facts separately from interpretations. Do not label a failure a confirmed defect until the group's agreed oracle supports that classification. Keep commands, branch/commit, test configuration, and saved output traceable. Do not modify the baseline SUT for these tests.

## Group-wide test setup (complete once / update if agreed configuration changes)

| Field | Value |
|---|---|
| Approved test oracle / reference | Pending group approval; expected refusal conditions are defined in the current test assertions and proposed Golden Set cases. |
| Oracle decision date / location | Pending |
| Approved Golden Set case IDs | Pending group approval; this record covers Marjan's G05, G06, G07. Other branches may use overlapping IDs. |
| Approved shared documents / versions | Pending formal approval; exact synthetic content reproduced below. |
| Embedding backend | `HashingEmbeddingBackend` in Marjan's tests |
| Embedding dimensions | 512 in Marjan's tests |
| `min_relevance` | 0.20 in Marjan's tests |
| `top_k` | 3 in Marjan's tests |
| Real LLM / offline testing decision | G05 uses deterministic retrieval preflight; G06 and G07 use PydanticAI `TestModel`. No real LLM was used in these recorded runs. Group-wide decision pending. |
| Baseline tag / commit | `baseline` / `b354c12` (project baseline reference; not reverified in these runs) |
| Additional pass/fail thresholds | No additional thresholds verified; refusal checks use `answered=False`, empty citations, and for G05 `REFUSAL_TEXT`. |

---

# Test Execution Record — MARJAN-GOLDEN-SET-01 (G05 and G06)

## 1. Identification

| Field | Value |
|---|---|
| Log entry ID | MARJAN-GOLDEN-SET-01 |
| Date and time (including timezone) | 2026-10-11; exact execution time not recorded (Sweden: CEST, UTC+02:00) |
| Tested by | Marjan Motafeghi |
| Risk area / testing technique | Insufficient evidence and refusal; deterministic preflight and simulated unsupported-answer validation |
| Test case ID(s) | G05, G06 (Marjan's current IDs) |
| Test method(s) / file | `test_golden_set.py`: `GoldenSetRefusalTests.test_g05_refuses_unrelated_question`; `GoldenSetRefusalTests.test_g06_insufficient_annual_allowance_evidence` |
| Branch | `test/golden-set-refusal-marjan` (working branch reported; exact checkout at execution not independently captured) |
| Commit hash (`git rev-parse HEAD`) | Pending verification |
| Baseline or extended suite | Extended Golden Set tests; only these two test methods were run in this command |

## 2. Environment and configuration

| Field | Value |
|---|---|
| Operating system | macOS (MacBook Air; exact version not captured) |
| Python version | Not recorded; verify using `python --version` |
| pytest version | Not applicable to recorded command (`unittest` was used) |
| Virtual environment | Project `.venv` activated |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.20 |
| `top_k` | 3 |
| Model / TestModel / FunctionModel / none | G05: no model invoked if retrieval preflight refuses; G06: `TestModel(call_tools=["retrieve"])` |
| External API calls (yes/no) | No external model calls allowed (`models.ALLOW_MODEL_REQUESTS = False` during tests); network traffic not independently monitored |
| Relevant dependency versions | Not recorded |

## 3. Test setup and oracle

**Shared test documents / synthetic data (exact content or file reference):**

The test creates two in-memory documents with these contents:

- `benefits.txt`: `Eligible employees receive twelve weeks of paid parental leave after six months of employment.`
- `expenses.txt`: `Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.`

**Original question / input:**

- **G05:** `Who won the 1978 World Cup?`
- **G06:** `What is the annual meal allowance?`

**Paraphrased question / transformed input (if applicable):**

Not applicable. G06 additionally injects a deliberately unsupported model output: `The annual meal allowance is 70 dollars.`

**Expected behaviour (answer / refuse / other):**

- **G05:** Refuse because neither shared document answers the unrelated question.
- **G06:** Refuse the simulated annual monetary claim because the document states only a *daily* amount.

**Expected source, evidence, citation or refusal reason:**

- **G05:** No supporting source; return the standard insufficient-evidence response.
- **G06:** `expenses.txt` contains `The daily meal allowance is 70 dollars.` That is a genuine quotation, but it does not support the claim that the *annual* allowance is 70 dollars.

**Test oracle (approved case, documented rule, metamorphic relation, etc.):**

Provisional oracle from Golden Set proposals and explicit assertions: the application must not accept an answer containing an unsupported claim. Formal group-wide approval and defect-classification criteria remain pending.

**Measurable pass condition(s):**

- **G05:** `answer.answered is False`; `answer.citations == []`; `answer.text == REFUSAL_TEXT`.
- **G06:** `answer.answered is False`; `answer.citations == []` after a `TestModel` provides the unsupported annual claim and an authentic quoted span.

**Scope of assertion (retrieval / agent output / citation / other):**

- **G05:** Final `answer_question()` refusal, reached through the retrieval preflight gate.
- **G06:** Final `answer_question()` validation of a simulated agent output with a real citation. This is **not** a test of a real LLM's answer-generation tendency.

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
| Related issue / PR | Marjan's Golden Set branch; PR number/URL not recorded |
| Status (open / under review / resolved) | Open — review pending |
| Date reviewed by group | Pending |

**Additional notes:** This execution occurred before G07 was added to the test class. Therefore the command collected only G05 and G06.

---

# Test Execution Record — MARJAN-GOLDEN-SET-02 (G07)

## 1. Identification

| Field | Value |
|---|---|
| Log entry ID | MARJAN-GOLDEN-SET-02 |
| Date and time (including timezone) | 2026-10-11; exact execution time not recorded (Sweden: CEST, UTC+02:00) |
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
| Python version | Not recorded; verify using `python --version` |
| pytest version | Not applicable to recorded command (`unittest` was used) |
| Virtual environment | Project `.venv` activated |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.20 |
| `top_k` | 3 |
| Model / TestModel / FunctionModel / none | PydanticAI `TestModel(call_tools=["retrieve"])` |
| External API calls (yes/no) | No external model calls allowed (`models.ALLOW_MODEL_REQUESTS = False` during test); network traffic not independently monitored |
| Relevant dependency versions | Not recorded |

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

## 4. Execution and actual results

**Exact command(s):**

```bash
python -m unittest test_golden_set.GoldenSetRefusalTests.test_g07_refuses_unsupported_parental_leave_amount -v
```a# Test Evidence Log — Marjan's Golden Set Tests

**Course:** DV033G  
**Project:** Typed Agentic RAG (PydanticAI)  
**Tested by:** Marjan Motafeghi  
**Date:** 2026-10-11  
**Branch:** `test/golden-set-refusal-marjan`  
**Test file:** `test_golden_set.py`

## 1. Identification

**Risk area:** Insufficient Evidence & Refusal  
**Test cases:** G05, G06, G07  
**Testing technique:** Golden Set testing with controlled model outputs.

## 2. Environment and Configuration

- **OS:** macOS
- **Framework:** Python unittest
- **Model:** PydanticAI TestModel (no real LLM)
- **Embedding:** HashingEmbeddingBackend, 512 dimensions
- **min_relevance:** 0.2
- **top_k:** 3
- **External API calls:** Disabled

## 3. Test Setup and Oracle

Two synthetic documents were used:

- `benefits.txt`: Twelve weeks of paid parental leave after six months of employment.
- `expenses.txt`: Expense reports within thirty days and a daily meal allowance of 70 dollars.

The expected behavior was to refuse questions when the documents did not contain enough evidence to support an answer.

| Test | Question | Expected |
|---|---|---|
| G05 | Who won the 1978 World Cup? | Refuse |
| G06 | What is the annual meal allowance? | Refuse unsupported annual amount |
| G07 | What is the parental leave benefit amount in dollars? | Refuse unsupported monetary amount |

**Pass condition:** `answered=False`, empty citations, and the defined refusal text.

**Oracle status:** Proposed expectations; pending group approval.

## 4. Execution and Results

**Commands used:**

```bash
python -m unittest test_golden_set.GoldenSetRefusalTests -v
python -m unittest test_golden_set.GoldenSetRefusalTests.test_g07_refuses_unsupported_parental_leave_amount -v
```

| Test | Result | Observation |
|---|---|---|
| G05 | PASS | System refused the unrelated question |
| G06 | FAIL | Simulated unsupported annual allowance was accepted |
| G07 | FAIL | Simulated unsupported parental leave amount was accepted |

## 5. Findings and Interpretation

G05 passed as expected.

G06 and G07 failed because the final answer validation accepted simulated answers containing information not supported by the documents.

These failures suggest a possible limitation in answer validation. They do not demonstrate that a real LLM generated these incorrect answers.

**Classification:** Unclassified — pending group oracle approval and independent review.

**Changes to SUT:** None.

## 6. Follow-up

- Review G06 and G07 with the group.
- Confirm the expected behavior and test oracle.
- Independently reproduce the failed tests.
- Decide whether the findings are defects or design limitations.

**Status:** Tests executed; group review pending.


**Result summary (number passed / failed / xfailed / xpassed / errors / subtests):**

1 test run: **0 passed, 1 failed**, 0 errors; `Ran 1 test in 0.014s`.

**Actual output / behaviour (include scores, top-ranked source and `enough_evidence` where relevant):**

```text
test_g07_refuses_unsupported_parental_leave_amount (test_golden_set.GoldenSetRefusalTests.test_g07_refuses_unsupported_parental_leave_amount) ... FAIL

FAIL: test_g07_refuses_unsupported_parental_leave_amount
AssertionError: True is not false : G07: The system must refuse an unsupported monetary amount.

Ran 1 test in 0.014s
FAILED (failures=1)
```

The assertion received `answer.answered=True`, whereas the test expected `False`. The exact retrieval score, ranked source list, and `enough_evidence` value were not separately printed in this run.

**Status:** **FAIL**.

**Evidence location (terminal output file, screenshot, CI URL, commit or log path):**

Terminal output was shared in the project discussion; a permanent raw output file or CI link has not yet been recorded.

**Reproduced by another group member? If yes, who and when:**

Not yet independently reproduced.

## 5. Findings and interpretation

**Expected vs actual difference:**

The test expected refusal of an unsupported monetary benefit. The system accepted the deliberately simulated answer of 5000 dollars with a citation containing only the leave duration.

**Possible cause (hypothesis, not yet verified):**

The citation-validation step appears to verify quote presence rather than semantic support for the claim. This resembles the G06 observation, but is a separate question and evidence source.

**Classification:** **Unclassified reproduced test failure**, pending group agreement on the oracle. Not yet a group-confirmed defect.

**Oracle-based rationale for classification:**

The test's expectation is explicit, but the group has not yet decided whether checking claim-level semantic support is part of the intended guardrail requirement.

**Known limitations / confounding factors:**

The output was injected through `TestModel`, not generated by a real LLM. This does not establish real-model hallucination rates. The result has not been independently reproduced by another group member. Exact commit, Python version, and raw log artifact remain to be recorded.

**Changes to SUT (none / temporary and reverted / other):**

No production `agent.py` or `rag.py` changes reported; test code only.

## 6. Follow-up

| Field | Value |
|---|---|
| Action required | Agree on oracle; independently reproduce G07; record environment, commit and permanent raw output; decide whether to add real-LLM exploratory checks |
| Responsible person | Marjan (test author); group/reviewer for approval |
| Related issue / PR | Marjan's Golden Set branch; PR number/URL not recorded |
| Status (open / under review / resolved) | Open — review pending |
| Date reviewed by group | Pending |

**Additional notes:** Christian's G03 also asks about the parental-leave monetary amount, but tests `retrieve_evidence()` and its `enough_evidence` flag. G07 tests the later final-answer validation stage. These are distinct assertions and should be identified clearly to avoid confusion over case IDs and scope.

---

## Group review checklist

- [ ] Test case IDs and shared document contents match the approved proposal sheet (approval pending).
- [x] Expected behaviour and measurable pass conditions were defined in test assertions before interpreting the captured results.
- [ ] Environment, commit hash, configuration and exact command are recorded (commands/configuration recorded; versions/hash pending).
- [ ] Test result and evidence are saved and traceable (results transcribed; permanent raw logs pending).
- [x] Retrieval behaviour is not confused with correctness of the generated answer.
- [x] A failed test is not automatically described as a confirmed defect.
- [ ] Any AI-assisted findings are independently reproduced before being reported as group-verified.
- [ ] Baseline SUT remains unchanged, or temporary modifications are documented and reverted (no SUT changes reported; independent verification pending).
