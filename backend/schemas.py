from pydantic import BaseModel, ConfigDict, field_validator
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

    @field_validator("name", mode="before")
    @classmethod
    def reject_null_name(cls, value):
        if value is None:
            raise ValueError("name cannot be null; omit it to leave the name unchanged")
        return value
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

    @field_validator("name", mode="before")
    @classmethod
    def reject_null_name(cls, value):
        if value is None:
            raise ValueError("name cannot be null; omit it to leave the name unchanged")
        return value
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

    @field_validator("title", "steps", "expected_result", mode="before")
    @classmethod
    def reject_null_required_fields(cls, value, info):
        if value is None:
            raise ValueError(f"{info.field_name} cannot be null; omit it to leave the value unchanged")
        return value
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

    @field_validator("name", "status", mode="before")
    @classmethod
    def reject_null_required_fields(cls, value, info):
        if value is None:
            raise ValueError(f"{info.field_name} cannot be null; omit it to leave the value unchanged")
        return value
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
# Import Report Schemas
class ImportResultItem(BaseModel):
    test_case_id: str
    status: ResultStatus
    notes: Optional[str] = None
    execution_time_ms: Optional[int] = None
class ImportReportRequest(BaseModel):
    reporter: str
    results: List[ImportResultItem]
class ImportReportResponse(BaseModel):
    imported_count: int
    failed_count: int
    errors: List[str]
