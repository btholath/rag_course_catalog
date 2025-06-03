# backend/tests/test_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_query_endpoint():
    payload = {
        "query": "What are the prerequisites for data science courses?"
    }
    response = client.post("/query", json=payload)
    
    # Basic checks; adapt based on your actual response structure
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)

def test_invalid_query_payload():
    response = client.post("/query", json={})
    assert response.status_code == 422  # Unprocessable Entity due to missing required fields
