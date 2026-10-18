from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from database import Base
import uuid
import enum
from datetime import datetime, timezone
def generate_uuid():
    return str(uuid.uuid4())
class RunStatus(str, enum.Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
class ResultStatus(str, enum.Enum):
    PASSED = "Passed"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    BLOCKED = "Blocked"
    ERROR = "Error" # Automation/Setup issue, not a product failure
class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    suites = relationship("TestSuite", back_populates="project", cascade="all, delete-orphan")
    runs = relationship("TestRun", back_populates="project", cascade="all, delete-orphan")
class TestSuite(Base):
    __tablename__ = "test_suites"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    project = relationship("Project", back_populates="suites")
    cases = relationship("TestCase", back_populates="suite", cascade="all, delete-orphan")
class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    suite_id = Column(String, ForeignKey("test_suites.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, index=True, nullable=False)
    preconditions = Column(Text, nullable=True)
    steps = Column(Text, nullable=False)
    expected_result = Column(Text, nullable=False)
    priority = Column(String, default="Medium")
    tags = Column(String, nullable=True) 
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    suite = relationship("TestSuite", back_populates="cases")
    results = relationship("TestResult", back_populates="test_case", cascade="all, delete-orphan")
class TestRun(Base):
    __tablename__ = "test_runs"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(Enum(RunStatus), default=RunStatus.PENDING, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    project = relationship("Project", back_populates="runs")
    results = relationship("TestResult", back_populates="test_run", cascade="all, delete-orphan")
class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    test_run_id = Column(String, ForeignKey("test_runs.id", ondelete="CASCADE"), nullable=False)
    test_case_id = Column(String, ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=False)
    test_case_version = Column(Integer, nullable=False) # Snapshot version at execution time
    status = Column(Enum(ResultStatus), nullable=False)
    notes = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    test_run = relationship("TestRun", back_populates="results")
    test_case = relationship("TestCase", back_populates="results")
