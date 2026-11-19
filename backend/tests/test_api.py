"""Tests that do not require downloading models or calling Gemini."""
from fastapi.testclient import TestClient
from app.main import app

def test_health():
    response = TestClient(app).get("/v1/health")
    assert response.status_code == 200
    assert response.json()["milestone"] == 1

def test_query_validation():
    response = TestClient(app).post("/v1/query", json={"question": "", "top_k": 5})
    assert response.status_code == 422

def test_upload_extension_rejected():
    response = TestClient(app).post("/v1/documents", files={"file": ("malware.exe", b"not executable")})
    assert response.status_code == 415
