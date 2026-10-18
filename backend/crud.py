from sqlalchemy.orm import Session
import models, schemas
def get_project(db: Session, project_id: str):
    return db.query(models.Project).filter(models.Project.id == project_id).first()
def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()
def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(name=project.name, description=project.description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
def update_project(db: Session, project_id: str, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if db_project:
        # Pydantic মডেল থেকে শুধু সেই ভ্যালুগুলো নেব যেগুলো ইউজার পাঠিয়েছে (exclude_unset=True)
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
