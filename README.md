# G6 Pydantic Agentic RAG Testing

Testing and evaluation of a Typed Agentic RAG system using PydanticAI, focusing on retrieval, grounding, citations and agent behaviour.

This repository is used for the practical testing project in the course **DV033G – Principles & Practices in Software Testing** at Mid Sweden University.

## System Under Test

The primary system under test consists of:

- `agent.py` – agent orchestration, retrieval decisions, grounding and citation validation and refusal behaviour.
- `rag.py` – document chunking, embeddings, vector storage, retrieval, document ingestion and URL validation.

The Streamlit user interface is outside the primary testing scope.

## Upstream Source

The system under test is based on the **Typed Agentic RAG with PydanticAI** example from the `Shubhamsaboo/awesome-llm-apps` repository:

`rag_tutorials/agentic_typed_rag_pydanticai`

Original project:
https://github.com/Shubhamsaboo/awesome-llm-apps

The initial versions of `agent.py`, `rag.py`, `test_typed_rag.py`, `requirements.txt` and `.env.example` were copied from the upstream project to establish the testing baseline.

Subsequent changes in this repository are part of Group 6's testing and evaluation work.

## License

The upstream project is licensed under the Apache License 2.0. See `LICENSE` for details.

## Setup and Test Reproduction

### Prerequisites

- Python 3.12.3 (version used in the documented test execution)
- Git
- A Python virtual environment

### Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/yasva/g6-pydantic-agentic-rag-testing.git
cd g6-pydantic-agentic-rag-testing
```

Create and activate a virtual environment on Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the application dependencies and the testing tools used in the documented execution:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest==9.1.1 pytest-cov==7.1.0
python -m pip install ruff==0.17.0
```

### Configuration

The `.env.example` file contains placeholders for `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`, along with an optional `RAG_MODEL` setting.

The documented deterministic tests use controlled model responses and local embeddings rather than live external model requests.

### Running the Tests

Run the original baseline tests:

```bash
python -m pytest test_typed_rag.py
```

Run the original and extended tests together, including coverage measurement:

```bash
python -m pytest test_typed_rag.py test_golden_set.py --cov=agent --cov=rag --cov-branch --cov-report=term
```

### Static Analysis

Ruff can be used to check the Python source code for potential issues without running the tests.

Run Ruff with:

```bash
python -m ruff check agent.py rag.py
```

### Documented Test Results

The combined test execution on 15 October 2026 produced:

- 21 collected tests
- 17 passed
- 4 failed: G03, G06, G07, and M04
- Approximately 81% statement coverage
- 78% combined statement/branch coverage

The four failures represent documented findings in the extended test suite. They should not be interpreted as installation failures.

### Test Evidence

The repository contains supporting documentation and execution evidence:

- `docs/baseline.md`
- `docs/baseline-windows.txt`
- `docs/golden-set-work-allocation.md`
- `docs/test-logs/coverage-baseline-2026-10-15.txt`
- `docs/test-logs/coverage-extended-2026-10-15.txt`

The recorded coverage executions used application revision `fb894b8fba719cdfa5bd04cb4481cdc2938f25ef`. The coverage evidence was committed in revision `bd6f266`.

For exact reproduction of the recorded results, use the documented application revision and testing-tool versions.
