"""ZTA KnowledgeAI Milestone 1 API. No authentication: localhost use only."""
from functools import lru_cache
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from .core import settings
from .rag import KnowledgeStore

app = FastAPI(title="ZTA KnowledgeAI", version="0.1.0", description="Local development RAG vertical slice. Not production ready.")

@lru_cache(maxsize=1)
def store() -> KnowledgeStore:
    return KnowledgeStore()

class Query(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=10)

@app.get("/v1/health")
def health():
    return {"status": "ok", "milestone": 1}

@app.post("/v1/documents", status_code=201)
async def upload(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith((".pdf", ".txt", ".md")):
        raise HTTPException(415, "Only PDF, TXT and MD are supported")
    content = await file.read(settings.max_upload_bytes + 1)
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(413, "File exceeds upload limit")
    try:
        return store().add(file.filename, content)
    except (ValueError, UnicodeDecodeError, RuntimeError) as exc:
        raise HTTPException(422, str(exc)) from exc

@app.get("/v1/documents")
def documents():
    return {"documents": store().list_documents()}

@app.post("/v1/query")
def query(body: Query):
    try:
        return store().answer(body.question, body.top_k)
    except Exception as exc:
        # Do not expose API keys or provider errors in responses.
        raise HTTPException(502, "Retrieval or generation failed; check server logs") from exc
