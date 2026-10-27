# Test Evidence Log — Yasaman Metamorphic Testing

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Purpose:** Record reproducible evidence for metamorphic retrieval tests, distinguishing observations from defect classification.

## Group-wide test setup

| Field                                | Value                                                                                     |
| ------------------------------------ | ----------------------------------------------------------------------------------------- |
| Proposed test oracle / reference     | Group proposal sheet; approval status for M04 not confirmed                               |
| Oracle decision date / location      | Not recorded; confirm with group                                                          |
| Approved Golden Set case IDs         | Confirm against group proposal sheet; M04 was proposed as optional                        |
| Approved shared documents / versions | Synthetic `benefits.txt` and `expenses.txt` contents reproduced below in test setup       |
| Embedding backend                    | `HashingEmbeddingBackend`                                                                 |
| Embedding dimensions                 | 512                                                                                       |
| `min_relevance`                      | 0.2                                                                                       |
| `top_k`                              | 4                                                                                         |
| Real LLM / offline testing decision  | Offline retrieval-only tests; no model request or external API call                       |
| Baseline tag / commit                | `baseline` — `b354c12`                                                                    |
| Additional pass/fail thresholds      | Both formulations must meet the asserted source, evidence-text and sufficiency conditions |

---

# Test Execution Record — G6-META-001

## 1. Identification

| Field                              | Value                                                                        |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| Log entry ID                       | G6-META-001                                                                  |
| Date and time (including timezone) | 2026-10-11 (CEST, UTC+02:00); exact time not recorded                        |
| Tested by                          | Yasaman                                                                      |
| Risk area / testing technique      | Metamorphic testing — paraphrase invariance                                  |
| Test case ID(s)                    | M01, M02, M04                                                                |
| Test method(s) / file              | `MetamorphicTests` in `test_golden_set.py`                                   |
| Branch                             | `metamorphic-testing-yasaman`                                                |
| Commit hash                        | Historical run commit not recorded; do not substitute the later merge commit |
| Baseline or extended suite         | Extended suite, metamorphic tests only                                       |

## 2. Environment and configuration

| Field                                    | Value                                              |
| ---------------------------------------- | -------------------------------------------------- |
| Operating system                         | Ubuntu 24.04.4 LTS (WSL), as recorded for this run |
| Python version                           | 3.12.3                                             |
| pytest version                           | 9.1.1                                              |
| Virtual environment                      | `.venv`                                            |
| Embedding backend                        | `HashingEmbeddingBackend`                          |
| Embedding dimensions                     | 512                                                |
| `min_relevance`                          | 0.2                                                |
| `top_k`                                  | 4                                                  |
| Model / TestModel / FunctionModel / none | None; retrieval-only                               |
| External API calls (yes/no)              | No                                                 |
| Relevant dependency versions             | Not recorded beyond Python and pytest              |

## 3. Test setup and oracle

**Shared synthetic documents (indexed in memory):**

`benefits.txt`:

> Eligible employees receive twelve weeks of paid parental leave after six months of employment.

`expenses.txt`:

> Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.

**Proposed metamorphic relation:** Rephrasing a question without changing the requested fact should preserve retrieval of the expected source and evidence and the evidence-sufficiency decision.

| Case | Original question                                                    | Paraphrase                                                          | Expected first source | Expected evidence text                    |
| ---- | -------------------------------------------------------------------- | ------------------------------------------------------------------- | --------------------- | ----------------------------------------- |
| M01  | How many weeks of paid parental leave do eligible employees receive? | What is the duration of paid parental leave for eligible employees? | `benefits.txt`        | `twelve weeks of paid parental leave`     |
| M02  | When must employees submit expense reports after business travel?    | How soon after business travel are expense reports due?             | `expenses.txt`        | `within thirty days`                      |
| M04  | What is the daily meal allowance?                                    | How much is the meal allowance per day?                             | `expenses.txt`        | `The daily meal allowance is 70 dollars.` |

**Expected behaviour and measurable pass conditions:** For each pair, both retrieval results must have `enough_evidence=True`, a nonempty chunk list, the expected source as the first chunk and the expected text in the first chunk. The asserted conditions are stricter than merely requiring equal sufficiency decisions.

**Test oracle:** Proposed metamorphic relation and assertions in `MetamorphicTests`; M04's final group approval is not established.

**Scope of assertion:** Retrieval and evidence-sufficiency decisions only. Generated answers, refusals and citations are **not** tested.

## 4. Execution and actual results

**Exact command:**

```bash
python -m pytest test_golden_set.py::MetamorphicTests -v
```

**Result summary:** 2 passed, 1 failed; no errors reported.

| Case | Status | Observation                                                           |
| ---- | ------ | --------------------------------------------------------------------- |
| M01  | PASS   | Both formulations met the asserted conditions                         |
| M02  | PASS   | Both formulations met the asserted conditions                         |
| M04  | FAIL   | Original: `enough_evidence=True`; paraphrase: `enough_evidence=False` |

**M04 diagnostic observations (from earlier diagnostic run):**

| Field                     | Original       | Paraphrase     |
| ------------------------- | -------------- | -------------- |
| First retrieved source    | `expenses.txt` | `expenses.txt` |
| Expected evidence present | Yes            | Yes            |
| `enough_evidence`         | `True`         | `False`        |

**Overall status:** FAIL (one of three cases failed).

**Evidence location:** Local pytest terminal output and this summary. Raw terminal output was not saved as a file.

**Reproduced by another group member?** Not recorded at the time of this execution; see the later independent review documented under G6-META-002.

## 5. Findings and interpretation

**Expected vs actual difference:** M04 expected sufficient evidence for both equivalent questions; only the original satisfied that condition.

**Possible cause (unverified hypothesis):** Relevance scoring and/or the `min_relevance` threshold may be sensitive to question wording. Scores were not recorded.

**Classification:** Unclassified — pending group review.

**Oracle-based rationale:** The observed outcome contradicts the proposed M04 relation, but the group has not yet confirmed whether the oracle establishes a SUT defect rather than a test or design limitation.

**Known limitations / confounding factors:** Retrieval-only scope; no generated-answer or citation assertions; no scores recorded; M04 was optional in the proposal; independent reproduction was pending at the time of execution; later completed as documented in G6-META-002.

**Changes to SUT:** None.

## 6. Follow-up

| Field                  | Value                                                                 |
| ---------------------- | --------------------------------------------------------------------- |
| Action required        | Review M04 oracle and investigate the differing sufficiency decisions |
| Responsible person     | Yasaman Vallaee / Group 6                                             |
| Related issue / PR     | Not yet recorded                                                      |
| Status                 | Open — awaiting group review                                          |
| Date reviewed by group | Pending                                                               |

---

# Test Execution Record — G6-META-002

## 1. Identification

| Field                              | Value                                                                                                         |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Log entry ID                       | G6-META-002                                                                                                   |
| Date and time (including timezone) | 2026-10-12 (CEST, UTC+02:00); exact execution time not recorded                                               |
| Tested by                          | Yasaman                                                                                                       |
| Risk area / testing technique      | Metamorphic testing — paraphrase invariance; full-suite regression check after merge                          |
| Test case ID(s)                    | M01, M02, M04; full suite also included Christian's G02 and G03 and 11 baseline tests                         |
| Test method(s) / file              | `MetamorphicTests`, `GoldenSetRetrievalTests` in `test_golden_set.py`; `TypedRagTests` in `test_typed_rag.py` |
| Branch                             | `metamorphic-testing-yasaman`                                                                                 |
| Commit hash (`git rev-parse HEAD`) | `de648f9a6348eaf39bc18a84bc04b9f063819360`                                                                    |
| Baseline or extended suite         | Baseline and extended suite, after merging `origin/main`                                                      |

## 2. Environment and configuration

| Field                                    | Value                                                                                                           |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Operating system                         | Linux under WSL; distribution version not rechecked during this run                                             |
| Python version                           | 3.12.3                                                                                                          |
| pytest version                           | 9.1.1                                                                                                           |
| Virtual environment                      | `.venv` (`/home/yasam/miun/DV033G-testing/project/g6-pydantic-agentic-rag-testing/.venv/bin/python`)            |
| Embedding backend                        | `HashingEmbeddingBackend` for M01, M02, M04, G02, G03                                                           |
| Embedding dimensions                     | 512 for those extended tests                                                                                    |
| `min_relevance`                          | 0.2 for those extended tests                                                                                    |
| `top_k`                                  | 4 for those extended tests                                                                                      |
| Model / TestModel / FunctionModel / none | None for the five extended retrieval tests; baseline suite includes its own test-model checks                   |
| External API calls (yes/no)              | No external API calls in the extended retrieval tests; not independently audited for every baseline test        |
| Relevant dependency versions             | `pluggy 1.6.0`, `logfire 5.1.1`, `anyio 4.15.1`, `platformdirs 4.12.3`, `pytest-cov 7.1.0` (pytest plugin list) |

## 3. Test setup and oracle

**Shared documents, metamorphic inputs and pass conditions:** Same as G6-META-001 above, with in-memory documents indexed afresh per test.

**Expected behaviour:** M01, M02 and M04 each satisfy the source, evidence-text and `enough_evidence=True` assertions for both question formulations.

**Test oracle:** Proposed paraphrase-invariance relation; final approval of M04 is pending group confirmation.

**Scope of assertion:** The metamorphic tests assert retrieval and evidence sufficiency only, not generated answers or citations. The full-suite run also executes separate baseline and Golden Set tests.

## 4. Execution and actual results

**Exact command:**

```bash
python -m pytest test_typed_rag.py test_golden_set.py -v
```

**Result summary:** **16 collected; 14 passed, 2 failed, 5 subtests passed; no errors reported.** Runtime: 3.00 seconds.

| Area / case                         | Status | Observation                                                                                                             |
| ----------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------- |
| Baseline `TypedRagTests` (11 tests) | PASS   | All 11 passed; pytest also reported 5 passing subtests                                                                  |
| Christian G02                       | PASS   | Expected expense-report retrieval assertions passed                                                                     |
| Christian G03                       | FAIL   | Expected `enough_evidence=False`, observed `True`                                                                       |
| Yasaman M01                         | PASS   | Both formulations satisfied assertions                                                                                  |
| Yasaman M02                         | PASS   | Both formulations satisfied assertions                                                                                  |
| Yasaman M04                         | FAIL   | `self.assertTrue(result.enough_evidence)` failed; earlier diagnostic run identified the paraphrase as returning `False` |

**M04 diagnostic context:** In the earlier diagnostic run, both formulations returned `expenses.txt` first and included the expected allowance sentence, but original and paraphrase differed on `enough_evidence` (`True` versus `False`). The 2026-10-12 full-suite output confirms M04 failed at the sufficiency assertion; it did not print scores or individual retrieval results.

**Overall status:** FAIL (two tests failed in the full suite; **one of the three Yasaman metamorphic tests** failed).

**Evidence location:** Local terminal output pasted into the project conversation; this log records its summary. No raw-output file or CI run link recorded.

**Reproduced by another group member?** Not recorded at the time of this execution. M01, M02 and M04 were subsequently independently reproduced by Marjan Motafeghizenoz on macOS, Python 3.12.6, at commit 3ab25e6. The results were M01 PASS, M02 PASS and M04 FAIL. See marjan-review-yasaman.md.

## 5. Findings and interpretation

**Expected vs actual difference (M04):** The test requires sufficient evidence for both phrasings; at least one returned `False`, consistent with the earlier diagnostic showing the paraphrase fails.

**Separate observation (G03):** Christian's test expects a question about the monetary amount of parental-leave benefits to have insufficient evidence, but `retrieve_evidence()` returned `enough_evidence=True`. This is a separate Golden Set finding and is **not** counted as a Yasaman metamorphic failure.

**Possible cause (unverified hypothesis):** Retrieval relevance or threshold behaviour may produce evidence-sufficiency decisions that do not match the intended semantic oracle. No causal analysis or score trace was recorded during this execution. A later diagnostic score trace is documented in G6-META-003.

**Classification:** M04 unclassified — pending group review. G03 classification belongs to the group's Golden Set review.

**Oracle-based rationale:** A failed assertion is a reproducible observation, not by itself a confirmed SUT defect. Group approval of the expected behaviour and review of test design are needed.

**Known limitations / confounding factors:** Retrieval-only metamorphic checks; scores not logged; no independent replication at the time of execution; subsequently reproduced by Marjan; M04 optional in the proposal; no final group oracle decision recorded.

**Changes to SUT:** None.

## 6. Follow-up

| Field                  | Value                                                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Action required        | Review M04's oracle and evidence-sufficiency mismatch; coordinate separately with Christian on G03; preserve failing tests and outputs |
| Responsible person     | Yasaman (M04), Christian / Group 6 (G03)                                                                                               |
| Related issue / PR     | Not yet recorded                                                                                                                       |
| Status                 | Open — awaiting group review                                                                                                           |
| Date reviewed by group | Pending                                                                                                                                |

**Additional notes:** The test file contains both Christian's `GoldenSetRetrievalTests` and Yasaman's `MetamorphicTests` after merging `origin/main`. The run used commit de648f9 together with an uncommitted import cleanup. Therefore, the recorded commit alone does not represent the complete executed working-tree state.

---

## Group review checklist

- [ ] Test case IDs and shared document contents match the approved proposal sheet (M04 approval still to confirm).
- [ ] Expected behaviour and measurable pass conditions are accepted by the group.
- [x] Environment, HEAD commit, configuration and exact test command recorded for the 2026-10-12 run; import cleanup was uncommitted.
- [ ] Raw test output saved to a traceable file or CI artifact (currently summarized from terminal output).
- [x] Retrieval behaviour distinguished from correctness of generated answers.
- [x] Failures not automatically labelled confirmed defects.
- [x] M01, M02 and M04 independently reproduced by Marjan Motafeghizenoz; see `marjan-review-yasaman.md`. This confirms the observed test outcomes, not the classification of M04 as a software defect.
- [x] No SUT changes made for these tests.

---

# Additional Diagnostic Execution — G6-META-003

## 1. Identification

| Field                      | Value                                                  |
| -------------------------- | ------------------------------------------------------ |
| Log entry ID               | G6-META-003                                            |
| Date                       | 2026-10-27 (CET, UTC+01:00); exact time not recorded   |
| Tested by                  | Yasaman Vallaee                                        |
| Purpose                    | Record retrieval similarity scores for G03/G07 and M04 |
| Tested commit              | `8c2842f6aadca2baaa1637f8ffa18987182f28ec`             |
| Evidence commit            | `29f972b`                                              |
| Branch containing evidence | `test/score-trace`                                     |

## 2. Environment and configuration

| Field                | Value                        |
| -------------------- | ---------------------------- |
| Operating system     | Linux, WSL2                  |
| Python version       | 3.12.3                       |
| Embedding backend    | `HashingEmbeddingBackend`    |
| Embedding dimensions | 512                          |
| `min_relevance`      | 0.2                          |
| `top_k`              | 4                            |
| External API calls   | None; `OPENAI_API_KEY` unset |

## 3. Test setup and oracle

The diagnostic script indexed the same two synthetic documents used by the Golden Set and metamorphic tests. It measured retrieval similarity scores and evidence-sufficiency decisions without generating model answers.

The M04 expectation was that meaning-preserving paraphrases should retain the expected source and sufficient-evidence decision.

## 4. Execution and actual results

**Exact command:**

```bash
env -u OPENAI_API_KEY python score_trace.py | tee docs/test-logs/score-trace-2026-10-27.txt
```

| Question       | First retrieved source | Similarity score | `enough_evidence` |
| -------------- | ---------------------- | ---------------: | ----------------- |
| G03/G07        | `benefits.txt`         |           0.2182 | `True`            |
| M04 original   | `expenses.txt`         |           0.4303 | `True`            |
| M04 paraphrase | `expenses.txt`         |           0.1925 | `False`           |

**Evidence location:** `docs/test-logs/score-trace-2026-10-27.txt`

**Reproducibility:** The saved output records the tested commit, Python version, operating system, indexed chunks and retrieval results.

## 5. Findings and interpretation

Both M04 formulations retrieved `expenses.txt` as the first source, but their similarity scores fell on opposite sides of the configured threshold of 0.2. Consequently, the original question returned `enough_evidence=True`, while the paraphrase returned `False`.

The diagnostic results support the observed M04 failure and demonstrate sensitivity to question wording in the offline hashing-based retrieval configuration.

These results do not establish that the same behaviour occurs with OpenAI embeddings or generated model answers.

The G03/G07 diagnostic also recorded `enough_evidence=True` for a question requesting a monetary parental-leave amount that is absent from the synthetic documents. This is supporting evidence for the separate Golden Set finding, not an additional metamorphic test failure.

**Classification:** M04 remains unclassified pending a formal decision about the proposed oracle.

**Changes to SUT:** None. A Git comparison confirmed that `agent.py` and `rag.py` were unchanged between the October 15 revision `fb894b8` and the diagnostic revision `8c2842f`.

## 6. Follow-up

The diagnostic script and saved output were committed to branch `test/score-trace` in commit `29f972b`.

This diagnostic execution supplements the original October 11–12 test records. It does not replace those runs or change their reported test counts.
