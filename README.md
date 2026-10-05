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