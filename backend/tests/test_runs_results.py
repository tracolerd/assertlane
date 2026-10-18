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
def base_data():
    project = client.post("/api/projects/", json={"name": "Run Project"}).json()
    suite = client.post(f"/api/projects/{project['id']}/suites/", json={"name": "Run Suite"}).json()
    case = client.post(
        f"/api/suites/{suite['id']}/cases/",
        json={"title": "Test Login", "steps": "Step 1", "expected_result": "Result 1"}
    ).json()
    return {"project_id": project["id"], "suite_id": suite["id"], "case_id": case["id"]}
@pytest.fixture
def test_run(base_data):
    run = client.post(f"/api/projects/{base_data['project_id']}/runs/", json={"name": "Release 1.0"}).json()
    return run
def test_create_and_update_run(base_data):
    # Create Run
    run_response = client.post(
        f"/api/projects/{base_data['project_id']}/runs/",
        json={"name": "Sprint 5"}
    )
    assert run_response.status_code == 201
    run_data = run_response.json()
    assert run_data["status"] == "Pending"
    assert run_data["started_at"] is None
    # Update to Running
    update_response = client.patch(
        f"/api/runs/{run_data['id']}",
        json={"status": "Running"}
    )
    assert update_response.status_code == 200
    updated_run = update_response.json()
    assert updated_run["status"] == "Running"
    assert updated_run["started_at"] is not None
def test_create_test_result_and_immutability(base_data, test_run):
    # Record a result
    result_response = client.post(
        f"/api/runs/{test_run['id']}/results/",
        json={
            "test_case_id": base_data["case_id"],
            "status": "Passed",
            "notes": "Looks good"
        }
    )
    assert result_response.status_code == 201
    result_data = result_response.json()
    assert result_data["test_case_version"] == 1
    assert result_data["status"] == "Passed"
    # Update original test case to bump version
    client.patch(f"/api/cases/{base_data['case_id']}", json={"steps": "Step 1, Step 2"})
    # Create another result for the same case but in a new run
    run2 = client.post(f"/api/projects/{base_data['project_id']}/runs/", json={"name": "Release 1.1"}).json()
    result_response_2 = client.post(
        f"/api/runs/{run2['id']}/results/",
        json={
            "test_case_id": base_data["case_id"],
            "status": "Failed"
        }
    )
    assert result_response_2.json()["test_case_version"] == 2
    # Check that old result is untouched
    old_results = client.get(f"/api/runs/{test_run['id']}/results/").json()
    assert old_results[0]["test_case_version"] == 1
