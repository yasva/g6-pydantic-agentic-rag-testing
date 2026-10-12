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
| Approved shared documents / versions | |
| Embedding backend | |
| Embedding dimensions | |
| `min_relevance` | |
| `top_k` | |
| Real LLM / offline testing decision | |
| Baseline tag / commit | |
| Additional pass/fail thresholds | |

---

# Test Execution Record — [COPY THIS SECTION FOR EACH RUN]

## 1. Identification

| Field | Value |
|---|---|
| Log entry ID | |
| Date and time (including timezone) | |
| Tested by | |
| Risk area / testing technique | |
| Test case ID(s) | |
| Test method(s) / file | |
| Branch | |
| Commit hash (`git rev-parse HEAD`) | |
| Baseline or extended suite | |

## 2. Environment and configuration

| Field | Value |
|---|---|
| Operating system | |
| Python version | |
| pytest version | |
| Virtual environment | |
| Embedding backend | |
| Embedding dimensions | |
| `min_relevance` | |
| `top_k` | |
| Model / TestModel / FunctionModel / none | |
| External API calls (yes/no) | |
| Relevant dependency versions | |

## 3. Test setup and oracle

**Shared test documents / synthetic data (exact content or file reference):**


**Original question / input:**


**Paraphrased question / transformed input (if applicable):**


**Expected behaviour (answer / refuse / other):**


**Expected source, evidence, citation or refusal reason:**


**Test oracle (approved case, documented rule, metamorphic relation, etc.):**


**Measurable pass condition(s):**


**Scope of assertion (retrieval / agent output / citation / other):**


## 4. Execution and actual results

**Exact command(s):**

```bash

```

**Result summary (number passed / failed / xfailed / xpassed / errors / subtests):**


**Actual output / behaviour (include scores, top-ranked source and `enough_evidence` where relevant):**


**Status:** PASS / FAIL / XFAIL / XPASS / ERROR / NOT RUN

**Evidence location (terminal output file, screenshot, CI URL, commit or log path):**


**Reproduced by another group member? If yes, who and when:**


## 5. Findings and interpretation

**Expected vs actual difference:**


**Possible cause (hypothesis, not yet verified):**


**Classification:** Unclassified / Confirmed defect / Design limitation / Test defect / No issue

**Oracle-based rationale for classification:**


**Known limitations / confounding factors:**


**Changes to SUT (none / temporary and reverted / other):**


## 6. Follow-up

| Field | Value |
|---|---|
| Action required | |
| Responsible person | |
| Related issue / PR | |
| Status (open / under review / resolved) | |
| Date reviewed by group | |

**Additional notes:**


---

## Group review checklist

- [ ] Test case IDs and shared document contents match the approved proposal sheet.
- [ ] Expected behaviour and measurable pass conditions were defined before interpreting results.
- [ ] Environment, commit hash, configuration and exact command are recorded.
- [ ] Test result and evidence are saved and traceable.
- [ ] Retrieval behaviour is not confused with correctness of the generated answer.
- [ ] A failed test is not automatically described as a confirmed defect.
- [ ] Any AI-assisted findings are independently reproduced before being reported as group-verified.
- [ ] Baseline SUT remains unchanged, or temporary modifications are documented and reverted.
