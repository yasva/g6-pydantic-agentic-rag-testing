# Test Evidence Log — Group 6

**Course:** DV033G — Principles & Practices in Software Testing  
**Project:** Typed Agentic RAG (PydanticAI)  
**Repository:** `g6-pydantic-agentic-rag-testing`  
**Purpose:** Record reproducible, independently verifiable evidence for the baseline and extended test suite.

> **Instructions:** Each group member copies the blank *Test Execution Record* below for each meaningful test run or finding. Record observed facts separately from interpretations. Do not label a failure a confirmed defect until the group's agreed oracle supports that classification. Keep commands, branch/commit, test configuration, and saved output traceable. Do not modify the baseline SUT for these tests.

## Group-wide test setup (complete once / update if agreed configuration changes)

| Field | Value |
|---|---|
| Approved test oracle / reference | |
| Oracle decision date / location | |
| Approved Golden Set case IDs | |
| Approved shared documents / versions | benefits.txt and expenses.txt |
| Embedding backend | HashingEmbeddingBackend |
| Embedding dimensions | 512 |
| `min_relevance` | 0.2 |
| `top_k` | ? |
| Real LLM / offline testing decision | Offline - TestModel used for G04. Retrieval only for G01 |
| Baseline tag / commit | 47eb704 |
| Additional pass/fail thresholds | |

---

# Test Execution Record 

## 1. Identification

| Field | Value |
|---|---|
| Log entry ID | |
| Date and time (including timezone) | G04 2026-10-09 - G01 1026-10-13 |
| Tested by | David |
| Risk area / testing technique | Unsupported answers and citations |
| Test case ID(s) | G01 G04 |
| Test method(s) / file | GoldenSetFalseCitation, GoldenSetRetrievalTests in test_golden_set.py |
| Branch | test-wrong-citation-david |
| Commit hash (`git rev-parse HEAD`) | f4ad281c001d00387534c23e022164f19835058d |
| Baseline or extended suite | Extended suite |

## 2. Environment and configuration

| Field | Value |
|---|---|
| Operating system | Windows 11 Pro |
| Python version | 3.14.7 |
| pytest version | 9.1.1 |
| Virtual environment | venv |
| Embedding backend | HashingEmbeddingBackend |
| Embedding dimensions | 512 |
| `min_relevance` | 0.2 |
| `top_k` | G04 = 3, G01 = 4 |
| Model / TestModel / FunctionModel / none | TestModel |
| External API calls (yes/no) | No |
| Relevant dependency versions |  anyio-4.15.1, logfire-5.1.1, platformdirs-4.12.3, cov-7.1.0, pluggy-1.6.0 |

## 3. Test setup and oracle

**Shared test documents / synthetic data (exact content or file reference):**

benefits.txt

expenses.txt

**Original question / input:**

G01 Question: How many weeks of paid parental leave do eligible employees receive?

G04 Question: What is the daily meal allowance?

**Paraphrased question / transformed input (if applicable):**


**Expected behaviour (answer / refuse / other):**

G01 answer

G04 refuse

**Expected source, evidence, citation or refusal reason:**

G01 benefits.txt

G04 none, the hallucinated source should not lead to an answer

**Test oracle (approved case, documented rule, metamorphic relation, etc.):**


**Measurable pass condition(s):**


**Scope of assertion (retrieval / agent output / citation / other):**


## 4. Execution and actual results

**Exact command(s):**

```bash
python -m pytest test_golden_set.py -v --cov=agent --cov=rag --cov-report=term-missing

```

**Result summary 2 passed, 0 failed**


**Actual output / behaviour (include scores, top-ranked source and `enough_evidence` where relevant):**

test_golden_set.py::GoldenSetRetrievalTests::test_g01_retrieves_parental_leave_duration  PASSED 
test_golden_set.py::GoldenSetFalseCitation::test_G04_not_answered_when_incorrect_source PASSED

**Status:** PASS / FAIL / XFAIL / XPASS / ERROR / NOT RUN

**Evidence location (terminal output file, screenshot, CI URL, commit or log path):**

Terminal output

**Reproduced by another group member? If yes, who and when:**


## 5. Findings and interpretation

**Expected vs actual difference:**

G01 - The result marked the evidence as sufficient
G04 - Handled the hallucinated source correct by clearing the citations and refuse to answer

**Possible cause (hypothesis, not yet verified):**


**Classification:** Unclassified / Confirmed defect / Design limitation / Test defect / No issue

**Oracle-based rationale for classification:**


**Known limitations / confounding factors:**

Retrieval only for G01 and TestModel only for G04. No actual LLM was involved

**Changes to SUT (none / temporary and reverted / other):**

None

## 6. Follow-up

| Field | Value |
|---|---|
| Action required | |
| Responsible person | |
| Related issue / PR | |
| Status (open / under review / resolved) | |
| Date reviewed by group | |

**Additional notes:**

**Group verification note (2026-10-30):**

The repository's `baseline` tag was independently checked using `git rev-parse baseline^{commit}` and resolves to `b354c12a55ce3033aec13dfcbcaa15c284cc6408`, matching Section 5 of the group report. The `47eb704` reference in the original test log has been preserved as recorded by the test author. Its relationship to the verified baseline has not been established. This note does not change the original test execution record.


---

## Group review checklist

- [x] Test case IDs and shared document contents match the approved proposal sheet.
- [x] Expected behaviour and measurable pass conditions were defined before interpreting results.
- [x] Environment, commit hash, configuration and exact command are recorded.
- [x] Test result and evidence are saved and traceable.
- [x] Retrieval behaviour is not confused with correctness of the generated answer.
- [ ] A failed test is not automatically described as a confirmed defect.
- [ ] Any AI-assisted findings are independently reproduced before being reported as group-verified.
- [x] Baseline SUT remains unchanged, or temporary modifications are documented and reverted.
