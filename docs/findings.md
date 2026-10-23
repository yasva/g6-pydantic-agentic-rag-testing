# Test Findings — Group 6

## 1. Purpose

This document summarizes the main findings from the extended testing of the Typed Agentic RAG system.

The testing focused on retrieval relevance, evidence sufficiency, groundedness, citation validation, refusal behaviour, and metamorphic consistency.

The findings are based on deterministic tests using local hashing embeddings and controlled model responses. They do not represent an evaluation of a live external language model.

## 2. Test Execution Summary

The combined test execution on 15 October 2026 produced:

| Metric | Result |
|---|---|
| Total tests | 21 |
| Passed | 17 |
| Failed | 4 |
| Failed cases | G03, G06, G07, M04 |
| Statement coverage | Approximately 81% |
| Combined statement and branch coverage | 78% |

The original baseline suite contained 11 passing tests. The extended suite added 10 tests.

The additional tests identified behavioural risks without increasing the rounded coverage percentages.

## 3. Main Findings

### G03 — Related Evidence Accepted as Sufficient

**Expected:** The system should identify that the available parental leave document does not specify a monetary payment amount.

**Observed:** The retrieval decision reported `enough_evidence=True`, although the retrieved document only described the duration and eligibility of parental leave.

**Finding:** A relevance score above the configured threshold does not guarantee that the retrieved evidence contains the specific information requested.

**Interpretation:** This is an evidence-sufficiency risk. The expected behaviour and intended retrieval contract require further review before classifying the failure as a confirmed defect.

### G06 — Unsupported Annual Meal Allowance

**Expected:** The system should refuse to provide an annual meal allowance amount or explain that the available evidence only specifies a daily allowance.

**Observed:** The controlled model response included an unsupported annual amount and an authentic quotation from the expense policy. The validation accepted the response.

**Finding:** An authentic citation does not necessarily support every factual claim in an answer.

**Interpretation:** The result demonstrates a gap between citation validity and semantic grounding. Whether this is an implementation defect or a design limitation remains open.

### G07 — Unsupported Parental Leave Payment

**Expected:** The system should reject an unsupported monetary claim about parental leave.

**Observed:** A controlled response containing an unsupported $5,000 payment claim was accepted despite citing genuine text about parental leave duration.

**Finding:** Citation validation can accept an answer containing an unsupported claim when the citation itself is valid.

**Interpretation:** This exposes a grounding-validation limitation. Its classification as a defect depends on the intended system requirements.

### M04 — Paraphrase Sensitivity

**Expected:** Two questions asking for the same daily meal allowance should produce consistent evidence-sufficiency decisions.

**Observed:** The two paraphrases produced different similarity scores:

- First question: 0.4303
- Second question: 0.1925
- Configured threshold: 0.20

Consequently, the retrieval decisions differed.

**Finding:** Small wording changes can affect similarity scores enough to change the retrieval decision.

**Interpretation:** This indicates a consistency risk in the local retrieval configuration. It does not establish that a live LLM would produce inconsistent final answers.

## 4. Important Passing Results

G05 passed: the system refused to answer an unrelated question about the 1978 World Cup when the shared documents provided no supporting evidence.

M01 and M02 passed: the tested paraphrases produced consistent retrieval decisions for their respective questions.

These passing cases demonstrate that the tested behaviours worked under the specified conditions, but do not guarantee the same results for all possible inputs.

## 5. Limitations

The evaluation used two small synthetic documents and local hashing embeddings.

Controlled model responses were used instead of live external LLM calls.

The Golden Set contains a limited number of scenarios and cannot establish general reliability across all possible documents and questions.

Some failed tests depend on oracle assumptions that require final group review.

Coverage measures code execution, not factual correctness or semantic grounding.

## 6. Conclusion

The extended tests provided additional evidence about retrieval and grounding risks that were not apparent from the original passing baseline suite.

The most important findings concern the distinction between relevant evidence and sufficient evidence, the limitations of citation validation, and the sensitivity of retrieval decisions to paraphrasing.

The four failing tests are documented evaluation findings. Their final classification as software defects, design limitations, or oracle mismatches requires confirmation of the intended requirements.

## 7. Supporting Evidence

- `test_golden_set.py`
- `docs/golden-set-work-allocation.md`
- `docs/test-logs/coverage-extended-2026-10-15.txt`
- Individual test evidence files in `docs/test-logs/`