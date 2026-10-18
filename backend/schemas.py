from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
class ProjectCreate(ProjectBase): pass
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
# TestSuite Schemas
class TestSuiteBase(BaseModel):
    name: str
    description: Optional[str] = None
class TestSuiteCreate(TestSuiteBase): pass
class TestSuiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
class TestSuiteResponse(TestSuiteBase):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
# TestCase Schemas
class TestCaseBase(BaseModel):
    title: str
    preconditions: Optional[str] = None
    steps: str
    expected_result: str
    priority: Optional[str] = "Medium"
    tags: Optional[str] = None
class TestCaseCreate(TestCaseBase): pass
class TestCaseUpdate(BaseModel):
    title: Optional[str] = None
    preconditions: Optional[str] = None
    steps: Optional[str] = None
    expected_result: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
class TestCaseResponse(TestCaseBase):
    id: str
    suite_id: str
    version: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
