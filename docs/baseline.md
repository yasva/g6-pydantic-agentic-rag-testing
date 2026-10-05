# Baseline Testing Analysis

## 1. Purpose

This document records the initial testing baseline for the Typed Agentic RAG system before Group 6 adds or modifies tests.

The baseline is based on the upstream implementation and test suite copied from the `Shubhamsaboo/awesome-llm-apps` repository.

Baseline Git tag:

```text
baseline
```

Baseline commit:

```text
b354c12
```

The purpose of the baseline is to provide reproducible before/after evidence for the testing project.

---

## 2. System Under Test

The primary system under test consists of:

- `agent.py`
  - agent orchestration
  - retrieval decisions
  - structured answers
  - citation validation
  - grounding validation
  - refusal behaviour

- `rag.py`
  - document chunking
  - embeddings
  - in-memory vector storage
  - retrieval and ranking
  - PDF ingestion
  - HTML processing
  - URL validation

The Streamlit user interface is outside the primary testing scope.

---

## 3. Baseline Environment

The baseline was executed using:

- Python 3.12.3
- pytest 9.1.1
- pytest-cov 7.1.0
- coverage 7.16.2
- Linux

Command:

```bash
pytest test_typed_rag.py -v --cov=agent --cov=rag --cov-report=term-missing
```

---

## 4. Existing Test Suite

The upstream test suite contains 11 test methods and 5 parameterized subtests.

The existing tests cover several different parts of the system.

| Existing test | Area | Approximate test level |
|---|---|---|
| `test_chunk_text_uses_stable_overlap` | Chunking | Unit |
| `test_local_store_ranks_relevant_evidence` | Retrieval/ranking | Component |
| `test_retrieve_evidence_reports_threshold_decision` | Retrieval threshold | Component |
| `test_pdf_text_is_extracted_and_indexed` | PDF ingestion → retrieval | Integration |
| `test_answer_model_requires_citations_when_answered` | Answer validation | Unit |
| `test_out_of_corpus_question_refuses_without_model_request` | Refusal behaviour | Component |
| `test_agent_calls_retrieve_and_returns_typed_cited_answer` | Agent → retrieval → structured answer | Integration with test model |
| `test_forged_citation_forces_refusal` | Grounding/citation validation | Integration with test model |
| `test_model_resolution_supports_both_providers` | Model configuration | Unit |
| `test_html_to_text_ignores_scripts_and_styles` | HTML processing | Unit |
| `test_private_docs_urls_are_rejected` | URL validation | Unit with subtests |

These classifications describe how the tests interact with the current implementation and may be refined during the project.

---

## 5. Baseline Results

All existing tests passed.

```text
11 passed, 5 subtests passed in 10.23s
```

Coverage:

| Module | Statements | Missing | Coverage |
|---|---:|---:|---:|
| `agent.py` | 115 | 13 | 89% |
| `rag.py` | 232 | 53 | 77% |
| **Total** | **347** | **66** | **81%** |

Uncovered lines reported by coverage:

```text
agent.py:
38, 55, 63, 160, 167-171, 210, 212, 228, 236

rag.py:
137, 139, 143, 150, 195, 223, 226-228, 231-232, 235-236,
241-243, 260, 264, 267-268, 282, 296, 303, 307, 318, 324,
344, 376, 415, 417, 425-430, 440-441, 446-462
```

Coverage is treated as supporting baseline evidence rather than the primary measure of system quality.

---

## 6. Existing Testing Strategy

The existing suite provides deterministic tests for important application and RAG behaviour.

It verifies, among other things:

- deterministic chunk overlap
- basic retrieval ranking
- relevance-threshold decisions
- PDF ingestion and indexing
- structured answer validation
- refusal for an out-of-corpus question
- invocation of the retrieval tool
- rejection of forged citations
- model-provider configuration
- HTML content processing
- rejection of private/local URLs

The agent tests use PydanticAI's `TestModel` rather than a real external language model. Real model requests are disabled during these tests.

This makes the tests deterministic and suitable for verifying application behaviour, but it also means that they do not directly evaluate the behaviour or quality of a real LLM.

---

## 7. Initial Testing Gaps

The baseline reveals several areas that are not systematically evaluated by the existing suite.

### Retrieval quality

The suite contains individual retrieval examples, but there is no versioned evaluation dataset containing multiple known questions and expected evidence.

This makes it difficult to measure retrieval quality across a broader set of cases.

### Grounded answer quality

The existing suite verifies that forged citations can be rejected, but it does not systematically evaluate whether generated answers remain supported by retrieved evidence across multiple questions.

### Robustness and consistency

There is no systematic evaluation of how the system behaves when a question is reformulated while preserving its meaning.

For example, the baseline does not measure whether paraphrased questions retrieve equivalent evidence or preserve the same core factual answer.

### Refusal reliability

The existing suite contains an out-of-corpus refusal test, but refusal behaviour is not evaluated across a broader collection of answerable and unanswerable questions.

### Real-model behaviour

The agent integration tests use a controlled `TestModel`.

Therefore, the baseline primarily evaluates the surrounding application logic rather than the behaviour of a real LLM.

---

## 8. Initial Quality Focus

Based on the baseline, the project will initially focus on four areas:

1. **Retrieval relevance**  
   Whether relevant evidence is retrieved for answerable questions.

2. **Groundedness and citation validity**  
   Whether answers and citations are supported by retrieved evidence.

3. **Refusal reliability**  
   Whether the system refuses to answer when sufficient supporting evidence is unavailable.

4. **Robustness and consistency**  
   Whether semantically equivalent questions preserve relevant evidence and the core factual answer.

These areas will later be mapped to the quality attributes used in the course material.

---

## 9. Test Oracle Strategy

Different parts of the system require different test oracles.

For deterministic application behaviour, expected behaviour can be derived from explicit system rules and validation constraints.

For evaluation of RAG behaviour, a controlled Golden Set can define:

- test documents
- questions
- expected facts
- expected evidence/source
- whether the question should be answerable or refused

For metamorphic testing, the oracle does not require identical natural-language output. Instead, expected relations can be defined between executions.

For example, a semantic paraphrase of a question should preserve:

- relevant evidence
- answerability
- the core factual answer

This allows AI behaviour to be evaluated without requiring identical generated text.

---

## 10. Baseline Conclusion

The existing test suite provides a useful deterministic baseline and already tests several important parts of the RAG application.

However, high statement coverage alone does not demonstrate the quality of an AI-based RAG system.

The main opportunity for the project is therefore not simply to increase coverage, but to extend the existing testing strategy with systematic behavioural evaluation, particularly through Golden Set and metamorphic testing.

The extended tests should make it easier to distinguish between:

- retrieval/application failures, where incorrect or insufficient evidence is selected and
- model/answer failures, where suitable evidence is available but the generated answer is incorrect or insufficiently grounded.