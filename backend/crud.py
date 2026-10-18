from sqlalchemy.orm import Session
import models, schemas
# Project CRUD
def get_project(db: Session, project_id: str):
    return db.query(models.Project).filter(models.Project.id == project_id).first()
def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()
def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
def update_project(db: Session, project_id: str, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if db_project:
        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project
def delete_project(db: Session, project_id: str):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project
# TestSuite CRUD
def get_test_suite(db: Session, suite_id: str):
    return db.query(models.TestSuite).filter(models.TestSuite.id == suite_id).first()
def get_test_suites(db: Session, project_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.TestSuite).filter(models.TestSuite.project_id == project_id).offset(skip).limit(limit).all()
def create_test_suite(db: Session, suite: schemas.TestSuiteCreate, project_id: str):
    db_suite = models.TestSuite(**suite.model_dump(), project_id=project_id)
    db.add(db_suite)
    db.commit()
    db.refresh(db_suite)
    return db_suite
def update_test_suite(db: Session, suite_id: str, suite_update: schemas.TestSuiteUpdate):
    db_suite = get_test_suite(db, suite_id)
    if db_suite:
        update_data = suite_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_suite, key, value)
        db.commit()
        db.refresh(db_suite)
    return db_suite
def delete_test_suite(db: Session, suite_id: str):
    db_suite = get_test_suite(db, suite_id)
    if db_suite:
        db.delete(db_suite)
        db.commit()
    return db_suite
# TestCase CRUD
def get_test_case(db: Session, case_id: str):
    return db.query(models.TestCase).filter(models.TestCase.id == case_id).first()
def get_test_cases(db: Session, suite_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.TestCase).filter(models.TestCase.suite_id == suite_id).offset(skip).limit(limit).all()
def create_test_case(db: Session, case_item: schemas.TestCaseCreate, suite_id: str):
    db_case = models.TestCase(**case_item.model_dump(), suite_id=suite_id)
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case
def update_test_case(db: Session, case_id: str, case_update: schemas.TestCaseUpdate):
    db_case = get_test_case(db, case_id)
    if db_case:
        update_data = case_update.model_dump(exclude_unset=True)
        # Version bump logic for critical fields
        critical_fields = ["steps", "expected_result", "preconditions"]
        if any(field in update_data for field in critical_fields):
            db_case.version += 1
        for key, value in update_data.items():
            setattr(db_case, key, value)
        db.commit()
        db.refresh(db_case)
    return db_case
def delete_test_case(db: Session, case_id: str):
    db_case = get_test_case(db, case_id)
    if db_case:
        db.delete(db_case)
        db.commit()
    return db_case
