import sys
import os
# backend ডিরেক্টরিকে path-এ যুক্ত করা হচ্ছে
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
# টেস্টিংয়ের জন্য আলাদা SQLite ডেটাবেস
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
def test_create_project():
    response = client.post(
        "/api/projects/",
        json={"name": "Test Project", "description": "This is a test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "This is a test"
    assert "id" in data
def test_read_projects():
    response = client.get("/api/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_update_project():
    create_response = client.post(
        "/api/projects/",
        json={"name": "Old Name"}
    )
    project_id = create_response.json()["id"]
    update_response = client.patch(
        f"/api/projects/{project_id}",
        json={"name": "New Name"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "New Name"
def test_delete_project():
    create_response = client.post(
        "/api/projects/",
        json={"name": "To be deleted"}
    )
    project_id = create_response.json()["id"]
    delete_response = client.delete(f"/api/projects/{project_id}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/api/projects/{project_id}")
    assert get_response.status_code == 404
