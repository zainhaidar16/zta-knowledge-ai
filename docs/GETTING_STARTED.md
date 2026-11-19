# Milestone 1 — Run locally

**Status:** Initial implementation; requires local validation. The GitHub commit does not establish that tests have passed.

## Requirements

- Python 3.11 or newer, 12 GB RAM recommended
- Internet for initial embedding model download and optional Gemini API
- No GPU required; no Docker required
- Gemini API key is optional: without it, query endpoint returns retrieved evidence rather than a generated answer

## Setup

From the repository root:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
pip install -r backend/requirements.txt
cp .env.example .env
# Windows PowerShell: Copy-Item .env.example .env
# Set GEMINI_API_KEY in .env if using hosted generation
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Example commands

```bash
curl -X POST http://127.0.0.1:8000/v1/documents -F 'file=@example.txt'
curl http://127.0.0.1:8000/v1/documents
curl -X POST http://127.0.0.1:8000/v1/query -H 'Content-Type: application/json' -d '{"question":"What does the document say?","top_k":3}'
```

First ingestion downloads a small sentence-transformer model. It may take time on CPU. Document data and vectors persist in `./data` (gitignored).

## Tests

```bash
PYTHONPATH=backend pytest backend/tests -q
# PowerShell: $env:PYTHONPATH='backend'; pytest backend/tests -q
```

## Current limits and next milestone

- **Local single-user prototype only.** No authentication, tenant isolation, document deletion, malware scanning, or production-ready ACL enforcement.
- Accepts PDF, UTF-8 TXT, and Markdown; scanned PDFs require OCR (not included).
- Fixed-size character chunking and dense-only retrieval; hybrid BM25, reranking and LangGraph are next milestones.
- Citations list retrieved passages, but automated claim-level citation verification is not yet implemented.
- Free-tier Gemini limits and privacy policies apply. Use synthetic or public test documents; do not upload sensitive records.
- Qdrant Local is embedded; run only one API process against the data directory.
- Model dimension is fixed at 384; changing embedding model requires a new collection or reindex.

Milestone 1 acceptance: run health endpoint, upload sample TXT/PDF, retrieve relevant passages, generate cited answer with a configured Gemini key, and run tests locally. These steps still require execution and verification.
