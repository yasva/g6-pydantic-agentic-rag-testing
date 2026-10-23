# Test Evidence Log — Independent Review of Yasaman's Tests

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Reviewer:** Marjan Motafeghi  
**Test owner:** Yasaman  
**Purpose:** Independently reproduce and review Yasaman's metamorphic tests without changing the system under test (SUT).

## Group-wide test setup

| Field | Value |
|---|---|
| Test oracle / reference | Golden Set ground-truth facts and metamorphic paraphrase-consistency relation, documented in final report Section 3 |
| Oracle reference | Final report, Section 3 |
| Golden Set case IDs | Final report lists G01–G07 and M01, M02, M04 |
| Shared documents / versions | Synthetic `benefits.txt` and `expenses.txt`, as described in final report Section 3 |
| Embedding backend | `HashingEmbeddingBackend` |
| Embedding dimensions | 512 |
| `min_relevance` | 0.2 |
| `top_k` | 4 |
| Real LLM / offline testing decision | Final report Section 1 documents the group decision to use offline, controlled tests without a live LLM |
| Baseline tag / commit | `baseline` / `b354c12` |
| Additional pass/fail thresholds | M04 uses `min_relevance=0.2` and the test assertions below; no other threshold documented |

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
| Suite | Extended tests and full-suite regression |

### 2. Environment and configuration

| Field | Value |
|---|---|
| Operating system | macOS |
| Python version | 3.12.6 |
| Test framework | `unittest` |
| pytest version | Not used in this review |
| Virtual environment | `.venv` |
| Embedding backend | `HashingEmbeddingBackend` (512 dimensions) |
| `min_relevance` / `top_k` | 0.2 / 4 |
| Model / TestModel / FunctionModel / none | None; retrieval-only tests |
| External API calls | No |
| Relevant dependency versions | Not separately recorded |

### 3. Test setup and oracle

**Shared test documents / synthetic data**

The tests use an in-memory vector store with two synthetic documents:

- `benefits.txt`: “Eligible employees receive twelve weeks of paid parental leave after six months of employment.”
- `expenses.txt`: “Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.”

**Original question / input — M04**

`What is the daily meal allowance?`

**Paraphrased question / transformed input — M04**

`How much is the meal allowance per day?`

**Expected behaviour**

Yasaman's metamorphic tests expect semantically equivalent questions to produce consistent retrieval results. In M04, both should return `enough_evidence=True`.

**Expected source and evidence**

Both questions should retrieve `expenses.txt`, including the daily meal allowance of 70 dollars.

**Test oracle**

The oracle comes from the implemented test assertions and the paraphrase-consistency relation described in final report Section 3. The synthetic documents provide known facts. The report treats failures as findings rather than confirmed defects.

**Oracle status:** Defined and documented in the final report.

**Measurable pass conditions**

- Both questions return `enough_evidence=True`.
- Relevant evidence is retrieved.
- The paraphrased question meets the same tested conditions as the original.

**Scope of assertion**

Retrieval only; no real-LLM answer generation or answer correctness is tested.

### 4. Execution and actual results

**Exact commands**

```bash
python -m unittest test_golden_set.MetamorphicTests -v
python -m unittest discover -v
grep -n -A 45 '^async def retrieve_evidence' agent.py
git status
```

**Result summary**

| Execution | Passed | Failed | Total |
|---|---:|---:|---:|
| Yasaman's metamorphic tests | 2 | 1 | 3 |
| Full test suite (at this recorded commit; historical run, not the final combined suite) | 14 | 2 | 16 |

**Individual metamorphic test results**

| Test | Result |
|---|---|
| M01 — Paraphrase invariance | PASS |
| M02 — Expense report paraphrase | PASS |
| M04 — Meal allowance paraphrase | FAIL |

The full-suite run also failed Christian's G03 test, separately from M04. The final report presents a later combined result of 17 passed and 4 failed across 21 tests; these are different execution snapshots and should not be conflated.

**Observed M04 results**

| Measurement | Original question | Paraphrased question |
|---|---|---|
| Top relevance score | 0.4303 | 0.1925 |
| Required threshold | 0.2 | 0.2 |
| Relevant source retrieved | `expenses.txt` | `expenses.txt` |
| `enough_evidence` | True | False |

Both questions retrieved the same relevant source, but the paraphrase fell below the threshold.

**Failure excerpt**

```text
AssertionError: False is not true
```

The assertion failed in `test_golden_set.py`, line 225, when checking `result.enough_evidence`.

**Status:** FAIL — M04 independently reproduced.

**Evidence location**

Terminal output from the independent `unittest` runs and diagnostic commands; no separate evidence-log file was created during that review.

**Independent reproduction**

Marjan reproduced M04 on macOS at commit `3ab25e636088ce8beacd9909853e11b7ee95f938`.

### 5. Findings and interpretation

**Expected vs actual difference**

M04 expected `enough_evidence=True` for both questions. The original returned `True`; the paraphrase returned `False`, despite retrieving the same document.

**Verified technical explanation**

```python
enough_evidence=bool(results and top_score >= deps.min_relevance)
```

The original score (0.4303) exceeded the 0.2 threshold; the paraphrased score (0.1925) did not.

**Possible cause / interpretation**

Hashing-based retrieval scores can be sensitive to wording, causing equivalent questions to fall on opposite sides of the threshold. Whether this is an unacceptable defect depends on agreed requirements.

**Classification:** Recorded as finding F04 / M04 in final report Section 3; not a confirmed software defect.

**Oracle-based rationale**

The test expectation was not met and the failure was independently reproduced. In final report Section 3, the group records this as finding F04 / M04, while noting that classification as a defect requires formally agreed expectations.

**Known limitations**

- Deterministic hashing-based embeddings, not semantic embeddings from an online service.
- No real LLM or generated-answer correctness evaluated.
- `enough_evidence` depends on a numerical threshold.

**Changes to SUT:** None.

The final Git status was:

```text
nothing to commit, working tree clean
```

### 6. Follow-up

| Field | Value |
|---|---|
| Action required | Preserve F04 / M04 as a documented finding |
| Responsible person | Yasaman (owner); Marjan (reviewer) |
| Related issue / PR | None recorded |
| Status | Independent review complete; finding documented in final report |

**Additional notes**

M04's failure and both relevance scores were independently reproduced. The final report records this as a finding rather than a confirmed defect.

---

## Group review checklist

- [x] Implemented test case IDs and shared document descriptions are consistent with the final report.
- [x] Expected behaviour and measurable pass conditions identified from existing tests.
- [x] Environment, commit, configuration, and commands recorded.
- [x] Test results reproduced and recorded in terminal output.
- [x] Retrieval distinguished from generated-answer correctness.
- [x] Failure not automatically classified as a defect.
- [x] M04 failure independently reproduced.
- [x] Baseline SUT unchanged.

**Final review status:** Independent execution completed; M04 is documented as finding F04 in the final report.
