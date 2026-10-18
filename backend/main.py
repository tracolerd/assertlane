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
@app.post("/api/projects/", response_model=schemas.ProjectResponse, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)
@app.get("/api/projects/", response_model=List[schemas.ProjectResponse])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)
@app.get("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def read_project(project_id: str, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
@app.patch("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: str, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db, project_id=project_id, project_update=project_update)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
@app.delete("/api/projects/{project_id}", status_code=204)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return None
