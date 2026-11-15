import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app

client = TestClient(app)


def test_dashboard_page():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Overview Dashboard" in response.text


def test_upload_page():
    response = client.get("/upload")
    assert response.status_code == 200
    assert "Upload Resume PDF" in response.text


def test_history_page():
    response = client.get("/history")
    assert response.status_code == 200
    assert "Analysis History" in response.text


def test_get_analyses_api():
    response = client.get("/api/analyses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
