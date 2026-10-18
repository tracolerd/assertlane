from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from models import RunStatus, ResultStatus
# Project
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
# TestSuite
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
# TestCase
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
# TestRun
class TestRunBase(BaseModel):
    name: str
class TestRunCreate(TestRunBase): pass
class TestRunUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[RunStatus] = None
class TestRunResponse(TestRunBase):
    id: str
    project_id: str
    status: RunStatus
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
# TestResult (Append Only)
class TestResultCreate(BaseModel):
    test_case_id: str
    status: ResultStatus
    notes: Optional[str] = None
    execution_time_ms: Optional[int] = None
class TestResultResponse(BaseModel):
    id: str
    test_run_id: str
    test_case_id: str
    test_case_version: int
    status: ResultStatus
    notes: Optional[str] = None
    execution_time_ms: Optional[int] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
