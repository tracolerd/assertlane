from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime, timezone
# Project CRUD
def get_project(db: Session, project_id: str): return db.query(models.Project).filter(models.Project.id == project_id).first()
def get_projects(db: Session, skip: int = 0, limit: int = 100): return db.query(models.Project).offset(skip).limit(limit).all()
def create_project(db: Session, project: schemas.ProjectCreate):
    db_item = models.Project(**project.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def update_project(db: Session, project_id: str, project_update: schemas.ProjectUpdate):
    db_item = get_project(db, project_id)
    if db_item:
        for key, value in project_update.model_dump(exclude_unset=True).items(): setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item
def delete_project(db: Session, project_id: str):
    db_item = get_project(db, project_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
# TestSuite CRUD
def get_test_suite(db: Session, suite_id: str): return db.query(models.TestSuite).filter(models.TestSuite.id == suite_id).first()
def get_test_suites(db: Session, project_id: str, skip: int = 0, limit: int = 100): return db.query(models.TestSuite).filter(models.TestSuite.project_id == project_id).offset(skip).limit(limit).all()
def create_test_suite(db: Session, suite: schemas.TestSuiteCreate, project_id: str):
    db_item = models.TestSuite(**suite.model_dump(), project_id=project_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def update_test_suite(db: Session, suite_id: str, suite_update: schemas.TestSuiteUpdate):
    db_item = get_test_suite(db, suite_id)
    if db_item:
        for key, value in suite_update.model_dump(exclude_unset=True).items(): setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item
def delete_test_suite(db: Session, suite_id: str):
    db_item = get_test_suite(db, suite_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
# TestCase CRUD
def get_test_case(db: Session, case_id: str): return db.query(models.TestCase).filter(models.TestCase.id == case_id).first()
def get_test_cases(db: Session, suite_id: str, skip: int = 0, limit: int = 100): return db.query(models.TestCase).filter(models.TestCase.suite_id == suite_id).offset(skip).limit(limit).all()
def create_test_case(db: Session, case_item: schemas.TestCaseCreate, suite_id: str):
    db_item = models.TestCase(**case_item.model_dump(), suite_id=suite_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def update_test_case(db: Session, case_id: str, case_update: schemas.TestCaseUpdate):
    db_item = get_test_case(db, case_id)
    if db_item:
        update_data = case_update.model_dump(exclude_unset=True)
        if any(field in update_data for field in ["steps", "expected_result", "preconditions"]):
            db_item.version += 1
        for key, value in update_data.items(): setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item
def delete_test_case(db: Session, case_id: str):
    db_item = get_test_case(db, case_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
# TestRun CRUD
def get_test_run(db: Session, run_id: str): return db.query(models.TestRun).filter(models.TestRun.id == run_id).first()
def get_test_runs(db: Session, project_id: str, skip: int = 0, limit: int = 100): return db.query(models.TestRun).filter(models.TestRun.project_id == project_id).offset(skip).limit(limit).all()
def create_test_run(db: Session, run_item: schemas.TestRunCreate, project_id: str):
    db_item = models.TestRun(**run_item.model_dump(), project_id=project_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def update_test_run(db: Session, run_id: str, run_update: schemas.TestRunUpdate):
    db_item = get_test_run(db, run_id)
    if db_item:
        update_data = run_update.model_dump(exclude_unset=True)
        if "status" in update_data:
            if update_data["status"] == models.RunStatus.RUNNING and not db_item.started_at:
                db_item.started_at = datetime.now(timezone.utc)
            elif update_data["status"] == models.RunStatus.COMPLETED and not db_item.ended_at:
                db_item.ended_at = datetime.now(timezone.utc)
        for key, value in update_data.items(): setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item
def delete_test_run(db: Session, run_id: str):
    db_item = get_test_run(db, run_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
# TestResult CRUD
def get_test_results(db: Session, run_id: str, skip: int = 0, limit: int = 100): return db.query(models.TestResult).filter(models.TestResult.test_run_id == run_id).offset(skip).limit(limit).all()
def create_test_result(db: Session, run_id: str, result_item: schemas.TestResultCreate):
    case = get_test_case(db, result_item.test_case_id)
    if not case: return None # Router will handle 404
    db_item = models.TestResult(
        test_run_id=run_id,
        test_case_id=case.id,
        test_case_version=case.version, # capturing snapshot version
        status=result_item.status,
        notes=result_item.notes,
        execution_time_ms=result_item.execution_time_ms
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
