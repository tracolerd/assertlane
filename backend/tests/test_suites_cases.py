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
def test_project():
    response = client.post("/api/projects/", json={"name": "Test Project for Suites"})
    return response.json()
@pytest.fixture
def test_suite(test_project):
    response = client.post(
        f"/api/projects/{test_project['id']}/suites/",
        json={"name": "Login Suite"}
    )
    return response.json()
def test_create_suite(test_project):
    response = client.post(
        f"/api/projects/{test_project['id']}/suites/",
        json={"name": "Payment Suite", "description": "Payment tests"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Payment Suite"
def test_create_case_and_versioning(test_suite):
    # Create Case
    response = client.post(
        f"/api/suites/{test_suite['id']}/cases/",
        json={
            "title": "Valid Login",
            "steps": "1. Enter username 2. Enter password",
            "expected_result": "Dashboard opens"
        }
    )
    assert response.status_code == 201
    case_data = response.json()
    assert case_data["version"] == 1
    case_id = case_data["id"]
    # Update critical field (steps) and check version bump
    update_response = client.patch(
        f"/api/cases/{case_id}",
        json={"steps": "1. Enter email 2. Enter password"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["version"] == 2
    # Update non-critical field (title) and check version remains same
    update_response_2 = client.patch(
        f"/api/cases/{case_id}",
        json={"title": "Valid Email Login"}
    )
    assert update_response_2.json()["version"] == 2
def test_cascade_delete(test_project, test_suite):
    # Create a case inside the suite
    case_response = client.post(
        f"/api/suites/{test_suite['id']}/cases/",
        json={
            "title": "To be cascade deleted",
            "steps": "step",
            "expected_result": "result"
        }
    )
    case_id = case_response.json()["id"]
    # Delete the parent project
    delete_response = client.delete(f"/api/projects/{test_project['id']}")
    assert delete_response.status_code == 204
    # Verify suite and case are also deleted (returns 404)
    assert client.get(f"/api/suites/{test_suite['id']}").status_code == 404
    assert client.get(f"/api/cases/{case_id}").status_code == 404
