# Test Evidence Log — Independent Review of Yasaman's Tests

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Reviewer:** Marjan Motafeghi  
**Test owner:** Yasaman  
**Purpose:** Independently reproduce and review Yasaman's metamorphic testing results without modifying the system under test.

## Group-wide test setup

| Field | Value |
|---|---|
| Approved test oracle / reference | Not yet approved by the group |
| Oracle decision date / location | Pending group decision |
| Approved Golden Set case IDs | Pending group approval |
| Approved shared documents / versions | Synthetic `benefits.txt` and `expenses.txt` used in the tests; formal group approval pending |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.2 |
| `top_k` | 4 |
| Real LLM / offline testing decision | Reviewed tests run offline without an LLM; group-wide decision not confirmed |
| Baseline tag / commit | `baseline` / `b354c12` |
| Additional pass/fail thresholds | No additional group-approved thresholds confirmed |

---

## Test Execution Record — Independent Review

### 1. Identification

| Field | Value |
|---|---|
| Log entry ID | G6-META-INDEPENDENT-001 |
| Date | October 2026 |
| Tested by | Marjan Motafeghi |
| Risk area / testing technique | Metamorphic testing — paraphrase consistency |
| Test case IDs | M01, M02, M04 |
| Test methods / file | `MetamorphicTests` in `test_golden_set.py` |
| Branch | `metamorphic-testing-yasaman` |
| Commit hash | `3ab25e636088ce8beacd9909853e11b7ee95f938` |
| Suite | Extended suite; full-suite regression also executed |

### 2. Environment and configuration

| Field | Value |
|---|---|
| Operating system | macOS |
| Python version | 3.12.6 |
| Test framework | `unittest` |
| pytest version | Not used for this independent execution |
| Virtual environment | `.venv` |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.2 |
| `top_k` | 4 |
| Model / TestModel / FunctionModel / none | None for the reviewed retrieval tests |
| External API calls | No |
| Relevant dependency versions | Not separately recorded |

### 3. Test setup and oracle

**Shared test documents / synthetic data**

The reviewed tests use an in-memory vector store containing synthetic documents. The following content was independently used to reproduce the M04 result:

`benefits.txt`:

> Eligible employees receive twelve weeks of paid parental leave after six months of employment.

`expenses.txt`:

> Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.

**Original question / input — M04**

`What is the daily meal allowance?`

**Paraphrased question / transformed input — M04**

`How much is the meal allowance per day?`

**Expected behaviour**

Yasaman's metamorphic tests check whether questions with the same meaning produce consistent retrieval results.

For M04, the test expects both questions to return `enough_evidence=True`.

**Expected source and evidence**

Both questions should retrieve the relevant evidence from `expenses.txt`, including the statement that the daily meal allowance is 70 dollars.

**Test oracle**

The test expectations are defined in Yasaman's test code and are based on the proposed metamorphic relation of paraphrase consistency.

However, the group has not yet formally approved the final test oracle, Golden Set cases, or defect-classification criteria.

The current expectations are therefore used to reproduce the tests, **not as a group-approved reference for confirming software defects**.

**Oracle status:** Pending group review and approval.

**Measurable pass conditions**

According to the existing M04 test assertions:

- Both questions must return `enough_evidence=True`.
- The expected relevant evidence must be retrieved.
- The paraphrased question must satisfy the same tested conditions as the original question.

**Scope of assertion**

Retrieval behaviour only. The tests do not evaluate generated answers from a real LLM.

### 4. Execution and actual results

**Exact commands**

Run Yasaman's tests:

```bash
python -m unittest test_golden_set.MetamorphicTests -v
```

Run the full test suite:

```bash
python -m unittest discover -v
```

Inspect the retrieval decision:

```bash
grep -n -A 45 '^async def retrieve_evidence' agent.py
```

Verify repository status:

```bash
git status
```

**Result summary**

| Execution | Passed | Failed | Total |
|---|---:|---:|---:|
| Yasaman's metamorphic tests | 2 | 1 | 3 |
| Full test suite | 14 | 2 | 16 |

**Individual metamorphic test results**

| Test | Result |
|---|---|
| M01 — Paraphrase invariance | PASS |
| M02 — Expense report paraphrase | PASS |
| M04 — Meal allowance paraphrase | FAIL |

The full suite also reported a failure in Christian's G03 test. That failure is separate from Yasaman's M04 test.

**Observed M04 results**

| Measurement | Original question | Paraphrased question |
|---|---|---|
| Top relevance score | 0.4303 | 0.1925 |
| Required threshold | 0.2 | 0.2 |
| Relevant source retrieved | `expenses.txt` | `expenses.txt` |
| `enough_evidence` | True | False |

Both questions retrieved the same relevant text from `expenses.txt`. However, the second question returned `enough_evidence=False`.

**Failure excerpt**

```text
AssertionError: False is not true
```

The failure occurred in `test_golden_set.py`, line 225, at the assertion checking `result.enough_evidence`.

**Status:** FAIL — M04 independently reproduced.

**Evidence location**

Terminal output from the independent `unittest` runs and diagnostic commands. No separate evidence-log file was created during this review.

**Independent reproduction**

Marjan independently reproduced Yasaman's reported M04 failure on macOS using commit `3ab25e636088ce8beacd9909853e11b7ee95f938`.

### 5. Findings and interpretation

**Expected vs actual difference**

M04 expects both paraphrased questions to return `enough_evidence=True`.

The original question returned `True`, but the paraphrased question returned `False`, even though both retrieved the relevant document.

**Verified technical explanation**

The retrieval function uses the following condition:

```python
enough_evidence=bool(results and top_score >= deps.min_relevance)
```

The original question received a relevance score of `0.4303`, which is above the threshold of `0.2`.

The paraphrased question received `0.1925`, which is below the threshold.

This explains why the two questions produced different `enough_evidence` values.

**Possible cause / interpretation**

The hashing-based retrieval score is sensitive to the wording of the question. This can cause semantically similar questions to fall on different sides of the relevance threshold.

This is a demonstrated difference in retrieval behaviour, but whether it is an unacceptable system defect depends on the group's agreed oracle and requirements.

**Classification:** Unclassified — pending group review.

**Oracle-based rationale**

The existing test expectation is not met, and the failure has been independently reproduced. However, the group has not yet approved the final oracle or defect-classification criteria.

Therefore, M04 is recorded as a failed test and an observed consistency issue, not a confirmed software defect.

**Known limitations**

- The tests use a deterministic hashing-based embedding backend.
- No real LLM is evaluated.
- The evidence flag depends on a numerical relevance threshold.
- The test does not establish whether the generated answer would be correct.
- The group-wide oracle is not yet approved.

**Changes to SUT:** None.

The final Git status was:

```text
nothing to commit, working tree clean
```

### 6. Follow-up

| Field | Value |
|---|---|
| Action required | Review the M04 expectation and relevance-threshold behaviour with the group |
| Responsible person | Yasaman (test owner); Marjan (independent reviewer) |
| Related issue / PR | No issue or PR recorded for this review |
| Status | Open — pending group review |
| Date reviewed by group | Not yet recorded |

**Additional notes**

The independent review reproduced the reported M04 failure and measured the relevance scores for both questions.

The test results should remain separate from any final defect classification until the group approves its oracle.

---

## Group review checklist

- [ ] Test case IDs and shared document contents match the approved proposal sheet.
- [x] Expected behaviour and measurable pass conditions were identified from the existing tests.
- [x] Environment, commit hash, configuration, and execution commands were recorded.
- [x] Test results were independently reproduced and recorded in terminal output.
- [x] Retrieval behaviour was distinguished from generated-answer correctness.
- [x] The failed test was not automatically classified as a confirmed defect.
- [x] The reported M04 failure was independently reproduced.
- [x] Baseline SUT remained unchanged.

**Final review status:** Independent execution completed. Group oracle approval and defect classification remain pending.