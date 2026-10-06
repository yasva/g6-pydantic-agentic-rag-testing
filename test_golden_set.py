# TEMPLATE: Golden Set and Metamorphic Tests
#
# This file is intentionally a preparation template and contains no executable
# tests yet.
#
# IMPORTANT — where to work:
# 1. Draft and discuss proposed cases in the shared Word document:
#    golden-set-proposals.docx in the group's shared OneDrive.
# 2. Do not add proposed cases to this Python file while the group is still
#    discussing them.
# 3. After the group agrees on the cases and pass conditions, implement the
#    approved automated tests HERE, in test_golden_set.py.
# 4. Keep the existing tests in test_typed_rag.py; add to them only if the group
#    decides an approved case belongs with those existing tests.
#
# Follow the work allocation in docs/golden-set-work-allocation.md.


# SHARED TEST DOCUMENTS
#
# Use these same synthetic documents when proposing initial cases:
#
# benefits.txt:
# "Eligible employees receive twelve weeks of paid parental leave after six
# months of employment."
#
# expenses.txt:
# "Employees must submit expense reports within thirty days after business
# travel. The daily meal allowance is 70 dollars."
#
# If a proposed case needs additional or conflicting information, describe the
# proposed change in the Word proposal sheet. The group must approve changes so
# all final tests use the same agreed test documents.


# WORK ALLOCATION — INITIAL PROPOSALS
#
# Christian — Retrieval relevance
# Propose 2–3 answerable questions. Specify the expected source and exact
# evidence. Consider a related question that might retrieve irrelevant
# information or evidence that does not actually answer the question.
#
# David — Unsupported answers and citations
# Propose 2–3 cases about unsupported answer claims or invalid citations, such
# as a wrong source or chunk ID. First review test_typed_rag.py: it already
# checks that a forged quote causes refusal. Suggest cases that extend, rather
# than needlessly duplicate, the existing coverage.
#
# Marjan — Insufficient evidence and refusal
# Propose 2–3 questions the documents cannot answer. Consider a question for
# which the documents provide only part of the requested information. State
# what is missing and why the system should refuse.
#
# Yasaman — Metamorphic testing
# Propose 2–3 pairs of questions with the same meaning but different wording.
# Identify the original question for each paraphrase. Both questions should
# retrieve the same relevant evidence and lead to the same answer/refusal
# decision; their answer wording does not need to be identical.
#
# The group may change these assignments. Collect proposals in the shared Word
# document, not in separate test suites or separate Python files.


# CASE TEMPLATE — USE THIS IN THE WORD PROPOSAL SHEET
#
# Copy one block for each proposed case:
#
# Provisional ID:                 G01, G02, ... or M01, M02, ... for paraphrases
# Proposed by:
# Risk addressed:
# Question:
# Expected behaviour:             answer / refuse
# Expected source:
# Expected evidence or reason to refuse:
# Pass condition:                 a clear, measurable condition
# Related original case ID:       for a paraphrase only
# Test-document change needed:    no / yes — describe the proposed change
#
# For a metamorphic pair, record both the original question and its paraphrase,
# and define one pass condition for the pair.


# STARTER CASES FROM THE WORK-ALLOCATION SHEET
#
# These are proposals for group review, not approved automated tests. Keep,
# revise, or replace them in the shared Word proposal sheet:
#
# G01 — How many weeks of paid parental leave do eligible employees receive?
# Expected: answer; benefits.txt; "twelve weeks of paid parental leave".
#
# G02 — How long must an employee work before becoming eligible for parental
# leave?
# Expected: answer; benefits.txt; "after six months of employment".
#
# G03 — When must employees submit expense reports after business travel?
# Expected: answer; expenses.txt; "within thirty days".
#
# G04 — What is the daily meal allowance?
# Expected: answer; expenses.txt; "70 dollars".
#
# G05 — Who won the 1978 World Cup?
# Expected: refuse; the answer is not in the shared test documents.
#
# G06 — What is the annual meal allowance?
# Expected: refuse or clearly state that the documents specify only a daily
# allowance, not an annual amount.
#
# G07 — What is the parental leave benefit amount in dollars?
# Expected: refuse; the documents give a duration in weeks, not a monetary
# amount. The current relevance threshold may incorrectly accept the related
# chunk. Treat that as a finding if confirmed; do not hide it by changing the
# expected result.
#
# M01 — What is the duration of paid parental leave for eligible employees?
# Expected: retrieve the same relevant evidence as G01.
#
# M03 — How soon after business travel are expense reports due?
# Expected: retrieve the same relevant evidence as G03.


# IMPORTANT — CITATION VALIDITY AND ANSWER SUPPORT
#
# The system checks whether a quoted span occurs in a stored text chunk. That
# does not automatically prove that every claim in the answer is supported.
# Agree separately on how to test citation validity and support for the whole
# answer. Do not assume the application already performs a check that has not
# been verified.


# WORK SEQUENCE
#
# TODO 1: Each member drafts 2–3 cases in their assigned risk area in the shared
#         Word proposal sheet.
# TODO 2: Review the expected evidence, answer/refusal decision, and pass
#         condition together.
# TODO 3: Remove duplicates and check that the cases cover all five planned
#         risks: incorrect/irrelevant retrieval, unsupported answers,
#         incorrect citations, answering without enough evidence, and
#         inconsistent behaviour for equivalent questions.
# TODO 4: Agree on and record the final cases and shared test documents.
# TODO 5: Implement only the approved automated tests in THIS file:
#         test_golden_set.py.
# TODO 6: Follow the deterministic test patterns in test_typed_rag.py and avoid
#         external API calls in automated tests where possible.
# TODO 7: Run the new tests and then the complete suite. Save the command,
#         environment, and results.
# TODO 8: Compare baseline and extended results in the same environment.
#         Record findings, blockers, limitations, and remaining work.
