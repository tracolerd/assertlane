import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
@pytest.fixture
def import_setup_data():
    project = client.post("/api/projects/", json={"name": "Import Project"}).json()
    suite = client.post(f"/api/projects/{project['id']}/suites/", json={"name": "Import Suite"}).json()
    case = client.post(
        f"/api/suites/{suite['id']}/cases/",
        json={"title": "Import Case", "steps": "step", "expected_result": "result"}
    ).json()
    run = client.post(f"/api/projects/{project['id']}/runs/", json={"name": "Import Run"}).json()
    return {"run_id": run["id"], "case_id": case["id"]}
def test_import_results(import_setup_data):
    run_id = import_setup_data["run_id"]
    case_id = import_setup_data["case_id"]
    payload = {
        "reporter": "playwright-local",
        "results": [
            {
                "test_case_id": case_id,
                "status": "Passed",
                "execution_time_ms": 1200
            },
            {
                "test_case_id": "invalid-id-123",
                "status": "Failed"
            }
        ]
    }
    response = client.post(f"/api/runs/{run_id}/import", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["imported_count"] == 1
    assert data["failed_count"] == 1
    assert "TestCase invalid-id-123 not found." in data["errors"][0]
    # Verify result is actually in DB
    results_response = client.get(f"/api/runs/{run_id}/results/")
    assert len(results_response.json()) == 1
    assert results_response.json()[0]["test_case_id"] == case_id
