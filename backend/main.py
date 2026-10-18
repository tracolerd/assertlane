from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import get_db
app = FastAPI(
    title="AssertLane API",
    description="Quality Engineering Platform API",
    version="0.1.0"
)
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "AssertLane backend is operational"}
# --- PROJECT ENDPOINTS ---
@app.post("/api/projects/", response_model=schemas.ProjectResponse, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)
@app.get("/api/projects/", response_model=List[schemas.ProjectResponse])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)
@app.get("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def read_project(project_id: str, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if not db_project: raise HTTPException(status_code=404, detail="Project not found")
    return db_project
@app.patch("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: str, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db, project_id=project_id, project_update=project_update)
    if not db_project: raise HTTPException(status_code=404, detail="Project not found")
    return db_project
@app.delete("/api/projects/{project_id}", status_code=204)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    if not crud.delete_project(db, project_id=project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return None
# --- TEST SUITE ENDPOINTS ---
@app.post("/api/projects/{project_id}/suites/", response_model=schemas.TestSuiteResponse, status_code=201)
def create_suite_for_project(project_id: str, suite: schemas.TestSuiteCreate, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id): raise HTTPException(status_code=404, detail="Project not found")
    return crud.create_test_suite(db=db, suite=suite, project_id=project_id)
@app.get("/api/projects/{project_id}/suites/", response_model=List[schemas.TestSuiteResponse])
def read_suites_for_project(project_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id): raise HTTPException(status_code=404, detail="Project not found")
    return crud.get_test_suites(db, project_id=project_id, skip=skip, limit=limit)
@app.get("/api/suites/{suite_id}", response_model=schemas.TestSuiteResponse)
def read_suite(suite_id: str, db: Session = Depends(get_db)):
    db_suite = crud.get_test_suite(db, suite_id=suite_id)
    if not db_suite: raise HTTPException(status_code=404, detail="Suite not found")
    return db_suite
@app.patch("/api/suites/{suite_id}", response_model=schemas.TestSuiteResponse)
def update_suite(suite_id: str, suite_update: schemas.TestSuiteUpdate, db: Session = Depends(get_db)):
    db_suite = crud.update_test_suite(db, suite_id=suite_id, suite_update=suite_update)
    if not db_suite: raise HTTPException(status_code=404, detail="Suite not found")
    return db_suite
@app.delete("/api/suites/{suite_id}", status_code=204)
def delete_suite(suite_id: str, db: Session = Depends(get_db)):
    if not crud.delete_test_suite(db, suite_id=suite_id):
        raise HTTPException(status_code=404, detail="Suite not found")
    return None
# --- TEST CASE ENDPOINTS ---
@app.post("/api/suites/{suite_id}/cases/", response_model=schemas.TestCaseResponse, status_code=201)
def create_case_for_suite(suite_id: str, case_item: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    if not crud.get_test_suite(db, suite_id): raise HTTPException(status_code=404, detail="Suite not found")
    return crud.create_test_case(db=db, case_item=case_item, suite_id=suite_id)
@app.get("/api/suites/{suite_id}/cases/", response_model=List[schemas.TestCaseResponse])
def read_cases_for_suite(suite_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not crud.get_test_suite(db, suite_id): raise HTTPException(status_code=404, detail="Suite not found")
    return crud.get_test_cases(db, suite_id=suite_id, skip=skip, limit=limit)
@app.get("/api/cases/{case_id}", response_model=schemas.TestCaseResponse)
def read_case(case_id: str, db: Session = Depends(get_db)):
    db_case = crud.get_test_case(db, case_id=case_id)
    if not db_case: raise HTTPException(status_code=404, detail="Case not found")
    return db_case
@app.patch("/api/cases/{case_id}", response_model=schemas.TestCaseResponse)
def update_case(case_id: str, case_update: schemas.TestCaseUpdate, db: Session = Depends(get_db)):
    db_case = crud.update_test_case(db, case_id=case_id, case_update=case_update)
    if not db_case: raise HTTPException(status_code=404, detail="Case not found")
    return db_case
@app.delete("/api/cases/{case_id}", status_code=204)
def delete_case(case_id: str, db: Session = Depends(get_db)):
    if not crud.delete_test_case(db, case_id=case_id):
        raise HTTPException(status_code=404, detail="Case not found")
    return None
