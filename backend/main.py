import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import get_db
app = FastAPI(title="AssertLane API", description="Quality Engineering Platform API", version="0.1.0")

# CORS only controls which browser origins may read API responses; it is not
# authentication or authorization. Configure comma-separated origins for each
# deployed frontend environment.
_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
_allowed_origins = [
    origin.strip()
    for origin in os.getenv("ASSERTLANE_CORS_ORIGINS", _default_origins).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
@app.get("/api/health")
def health_check(): return {"status": "ok", "message": "AssertLane backend is operational"}
# --- PROJECT ENDPOINTS ---
@app.post("/api/projects/", response_model=schemas.ProjectResponse, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)): return crud.create_project(db=db, project=project)
@app.get("/api/projects/", response_model=List[schemas.ProjectResponse])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)): return crud.get_projects(db, skip=skip, limit=limit)
@app.get("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def read_project(project_id: str, db: Session = Depends(get_db)):
    db_item = crud.get_project(db, project_id=project_id)
    if not db_item: raise HTTPException(status_code=404, detail="Project not found")
    return db_item
@app.patch("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: str, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_project(db, project_id=project_id, project_update=project_update)
    if not db_item: raise HTTPException(status_code=404, detail="Project not found")
    return db_item
@app.delete("/api/projects/{project_id}", status_code=204)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    if not crud.delete_project(db, project_id=project_id): raise HTTPException(status_code=404, detail="Project not found")
    return None
# --- TEST SUITE ENDPOINTS ---
@app.post("/api/projects/{project_id}/suites/", response_model=schemas.TestSuiteResponse, status_code=201)
def create_suite(project_id: str, suite: schemas.TestSuiteCreate, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id): raise HTTPException(status_code=404, detail="Project not found")
    return crud.create_test_suite(db=db, suite=suite, project_id=project_id)
@app.get("/api/projects/{project_id}/suites/", response_model=List[schemas.TestSuiteResponse])
def read_suites(project_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id): raise HTTPException(status_code=404, detail="Project not found")
    return crud.get_test_suites(db, project_id=project_id, skip=skip, limit=limit)
@app.get("/api/suites/{suite_id}", response_model=schemas.TestSuiteResponse)
def read_suite(suite_id: str, db: Session = Depends(get_db)):
    db_item = crud.get_test_suite(db, suite_id=suite_id)
    if not db_item: raise HTTPException(status_code=404, detail="Suite not found")
    return db_item
@app.patch("/api/suites/{suite_id}", response_model=schemas.TestSuiteResponse)
def update_suite(suite_id: str, suite_update: schemas.TestSuiteUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_test_suite(db, suite_id=suite_id, suite_update=suite_update)
    if not db_item: raise HTTPException(status_code=404, detail="Suite not found")
    return db_item
@app.delete("/api/suites/{suite_id}", status_code=204)
def delete_suite(suite_id: str, db: Session = Depends(get_db)):
    if not crud.delete_test_suite(db, suite_id=suite_id): raise HTTPException(status_code=404, detail="Suite not found")
    return None
# --- TEST CASE ENDPOINTS ---
@app.post("/api/suites/{suite_id}/cases/", response_model=schemas.TestCaseResponse, status_code=201)
def create_case(suite_id: str, case_item: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    if not crud.get_test_suite(db, suite_id): raise HTTPException(status_code=404, detail="Suite not found")
    return crud.create_test_case(db=db, case_item=case_item, suite_id=suite_id)
@app.get("/api/suites/{suite_id}/cases/", response_model=List[schemas.TestCaseResponse])
def read_cases(suite_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not crud.get_test_suite(db, suite_id): raise HTTPException(status_code=404, detail="Suite not found")
    return crud.get_test_cases(db, suite_id=suite_id, skip=skip, limit=limit)
@app.get("/api/cases/{case_id}", response_model=schemas.TestCaseResponse)
def read_case(case_id: str, db: Session = Depends(get_db)):
    db_item = crud.get_test_case(db, case_id=case_id)
    if not db_item: raise HTTPException(status_code=404, detail="Case not found")
    return db_item
@app.patch("/api/cases/{case_id}", response_model=schemas.TestCaseResponse)
def update_case(case_id: str, case_update: schemas.TestCaseUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_test_case(db, case_id=case_id, case_update=case_update)
    if not db_item: raise HTTPException(status_code=404, detail="Case not found")
    return db_item
@app.delete("/api/cases/{case_id}", status_code=204)
def delete_case(case_id: str, db: Session = Depends(get_db)):
    if not crud.delete_test_case(db, case_id=case_id): raise HTTPException(status_code=404, detail="Case not found")
    return None
# --- TEST RUN ENDPOINTS ---
@app.post("/api/projects/{project_id}/runs/", response_model=schemas.TestRunResponse, status_code=201)
def create_run(project_id: str, run_item: schemas.TestRunCreate, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id): raise HTTPException(status_code=404, detail="Project not found")
    return crud.create_test_run(db=db, run_item=run_item, project_id=project_id)
@app.get("/api/projects/{project_id}/runs/", response_model=List[schemas.TestRunResponse])
def read_runs(project_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id): raise HTTPException(status_code=404, detail="Project not found")
    return crud.get_test_runs(db, project_id=project_id, skip=skip, limit=limit)
@app.get("/api/runs/{run_id}", response_model=schemas.TestRunResponse)
def read_run(run_id: str, db: Session = Depends(get_db)):
    db_item = crud.get_test_run(db, run_id=run_id)
    if not db_item: raise HTTPException(status_code=404, detail="Test Run not found")
    return db_item
@app.patch("/api/runs/{run_id}", response_model=schemas.TestRunResponse)
def update_run(run_id: str, run_update: schemas.TestRunUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_test_run(db, run_id=run_id, run_update=run_update)
    if not db_item: raise HTTPException(status_code=404, detail="Test Run not found")
    return db_item
@app.delete("/api/runs/{run_id}", status_code=204)
def delete_run(run_id: str, db: Session = Depends(get_db)):
    if not crud.delete_test_run(db, run_id=run_id): raise HTTPException(status_code=404, detail="Test Run not found")
    return None
# --- TEST RESULT ENDPOINTS ---
@app.post("/api/runs/{run_id}/results/", response_model=schemas.TestResultResponse, status_code=201)
def create_result(run_id: str, result_item: schemas.TestResultCreate, db: Session = Depends(get_db)):
    run = crud.get_test_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Test Run not found")
    case = crud.get_test_case(db, result_item.test_case_id)
    if not case:
        raise HTTPException(status_code=404, detail="TestCase not found")
    if not crud.test_case_matches_run_project(db, run_id, case.id):
        raise HTTPException(
            status_code=422,
            detail="Test case does not belong to the project associated with this test run.",
        )
    db_result = crud.create_test_result(db=db, run_id=run_id, result_item=result_item)
    if not db_result:
        raise HTTPException(status_code=422, detail="Test result violates project/run/case relationship integrity.")
    return db_result
@app.get("/api/runs/{run_id}/results/", response_model=List[schemas.TestResultResponse])
def read_results(run_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not crud.get_test_run(db, run_id): raise HTTPException(status_code=404, detail="Test Run not found")
    return crud.get_test_results(db, run_id=run_id, skip=skip, limit=limit)
@app.post("/api/runs/{run_id}/import", response_model=schemas.ImportReportResponse, status_code=201)
def import_results(run_id: str, report: schemas.ImportReportRequest, db: Session = Depends(get_db)):
    if not crud.get_test_run(db, run_id):
        raise HTTPException(status_code=404, detail="Test Run not found")
    return crud.import_test_results(db=db, run_id=run_id, report=report)
from fastapi.responses import HTMLResponse
@app.get("/demo", response_class=HTMLResponse)
def get_demo_page():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AssertLane Demo</title>
        </head>
        <body>
            <h1>Welcome to AssertLane</h1>
            <p>This is a local demo target for Playwright automation tests.</p>
            <button id="test-button">Click Me</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
