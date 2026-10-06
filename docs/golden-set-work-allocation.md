# Golden Set and Metamorphic Testing — Group Work Sheet

## Purpose

Use this sheet to prepare one shared, repeatable set of tests for the Typed Agentic RAG system. Each member proposes cases for an assigned risk area. The group then reviews the expected results together and combines the approved cases into one Golden Set.

Do not create four separate test suites. Use the same test documents and the same rules for deciding whether a result passes.

## Scope

Focus on:

- retrieving relevant evidence rather than irrelevant information
- answers being supported by the indexed documents
- citations pointing to real evidence
- refusing when the documents do not contain enough evidence
- consistent retrieval and answerability for equivalent question wording

The Streamlit user interface is outside this test scope.

## Shared test documents

Use these small, synthetic test documents for the initial cases:

**benefits.txt**

> Eligible employees receive twelve weeks of paid parental leave after six months of employment.

**expenses.txt**

> Employees must submit expense reports within thirty days after business travel. The daily meal allowance is 70 dollars.

Everyone should use exactly these test documents for the first round. If a case needs extra or conflicting information, add it to the shared test documents and record the change here before implementing tests.

## Suggested work allocation

Each member drafts two or three cases in their area using the case template below. These are proposals, not separate deliverables. The whole group agrees on each expected result before it is treated as part of the Golden Set.

| Member    | Initial focus                     | Example cases to propose                                                                             |
| --------- | --------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Christian | Retrieval relevance               | Answerable questions; a question that might retrieve a related but irrelevant chunk                  |
| David     | Unsupported answers and citations | Unsupported claim; fabricated quote or incorrect source/chunk                                        |
| Marjan    | Insufficient evidence and refusal | Unanswerable question; question for which the shared test documents contain only part of the requested information |
| Yasaman   | Metamorphic testing               | Two or three meaning-preserving paraphrase pairs for answerable questions                            |

The group may swap these areas. Keep the final cases together in one shared list and remove duplicates.

## Case template

Copy this block for every proposed case:

```text
Case ID:
Risk addressed:
Question:
Expected behaviour: answer / refuse
Expected source and evidence (or reason to refuse):
Pass condition:
Related case ID, if this is a paraphrase:
```

## Starter cases

These examples can be kept, changed, or replaced after group review.

| ID  | Risk                      | Question                                                                    | Expected behaviour and evidence                                                                             |
| --- | ------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| G01 | Retrieval relevance       | How many weeks of paid parental leave do eligible employees receive?        | Answer; retrieve `benefits.txt` and evidence containing “twelve weeks of paid parental leave”.              |
| G02 | Retrieval relevance       | How long must an employee work before becoming eligible for parental leave? | Answer; retrieve `benefits.txt` and evidence containing “after six months of employment”.                   |
| G03 | Retrieval relevance       | When must employees submit expense reports after business travel?           | Answer; retrieve `expenses.txt` and evidence containing “within thirty days”.                               |
| G04 | Retrieval relevance       | What is the daily meal allowance?                                           | Answer; retrieve `expenses.txt` and evidence containing “70 dollars”.                                       |
| G05 | Insufficient evidence     | Who won the 1978 World Cup?                                                 | Refuse; the shared test documents contain no evidence for this answer.                                                    |
| G06 | Insufficient evidence     | What is the annual meal allowance?                                          | Refuse or clearly state that the shared test documents only give a daily allowance; it does not specify an annual amount. |
| G07 | Related but unsupported information | What is the parental leave benefit amount in dollars? | Refuse; the shared test documents give a leave duration in weeks, not a monetary amount. The current relevance threshold may incorrectly accept the related chunk. |
| M01 | Metamorphic pair with G01 | What is the duration of paid parental leave for eligible employees? | Answer; retrieve the same relevant evidence as G01. |
| M03 | Metamorphic pair with G03 | How soon after business travel are expense reports due?                     | Answer; retrieve the same relevant evidence as G03.                                                         |

For metamorphic pairs, do not require identical generated wording. Require the same answer/refusal decision and relevant evidence. Record any differences that matter.

## Important distinction: citation validity and answer support

The current system checks whether a citation refers to a stored chunk and whether the quoted span occurs in that chunk. That is not automatically proof that every claim in the answer is supported by the quote.

If testing unsupported claims, define the expected behaviour precisely. For example, use a controlled test-model response containing one supported claim and one unsupported claim, then check whether the system rejects or otherwise flags it. Do not assume that the current implementation performs this check; report a failure as a finding rather than changing the expected result to make it pass.

Some citation cases may overlap with existing tests, including the forged-citation test in `test_typed_rag.py`. Prefer adding cases that broaden the existing test (for example, a wrong source or wrong chunk ID) rather than duplicating it without a reason.

## Group review checklist

Before implementing the cases, review them together:

- [ ] Every planned risk has at least one case.
- [ ] Each answerable case has a specific expected source and evidence.
- [ ] Each refusal case explains what evidence is missing.
- [ ] Each metamorphic case names its original case.
- [ ] Cases use the shared test documents and do not rely on external APIs or network access.
- [ ] Expected results are measurable and do not require exact natural-language answer matching.
- [ ] Existing tests have been checked so new cases add useful coverage rather than needless duplication.

## Work sequence

1. Each member drafts two or three cases in their assigned area using the template.
2. Put all proposals into this sheet or one shared copy of it.
3. Review the cases together, resolve ambiguous expected results, and remove duplicates.
4. Agree on the final Golden Set and record the final set of test documents.
5. Implement the approved cases as automated tests, using the project's existing deterministic test approach where possible.
6. Run the baseline version and the extended version with the same Python version, dependencies, operating system, and command for a fair before/after comparison.
7. Save the commands, test output, coverage results, findings, blockers, and remaining work as project evidence.

## Results log

Complete this after running the tests:

| Run                   | Revision/tag                         | OS and Python                                                     | Command                                                                                 | Result                                                                                                                                           | Evidence location                                    |
| --------------------- | ------------------------------------ | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Baseline              | `baseline` (commit `b354c12`)        | Linux, Python 3.12.3                                              | `pytest test_typed_rag.py -v --cov=agent --cov=rag --cov-report=term-missing`           | 11 passed, 5 parameterized subtests passed in 10.23s; coverage: agent 89% (115 statements), rag 77% (232 statements), total 81% (347 statements) | `docs/baseline.md`                                   |
| Baseline reproduction | Same project version as the baseline | Windows (`win32`), Python 3.12.10, pytest 9.1.1, pytest-cov 7.1.0 | `python -m pytest test_typed_rag.py -v --cov=agent --cov=rag --cov-report=term-missing` | 11 passed, 5 subtests passed in 8.43s; coverage: agent 89% (115 statements), rag 77% (232 statements), total 81% (347 statements)                | `docs/baseline-windows.txt` (local paths anonymized) |
| Extended suite        |                                      |                                                                   |                                                                                         |                                                                                                                                                  |                                                      |

Record separately:

- **Findings:** cases that failed and what the observed behaviour was.
- **Blockers:** setup or environment problems that prevented a test from running.
- **Limitations:** behaviours not evaluated, including the fact that deterministic test-model runs do not measure the quality of a live LLM.
- **Remaining work:** cases or evidence still to complete.
