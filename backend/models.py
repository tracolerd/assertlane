from sqlalchemy import Column, String, DateTime, Text
from database import Base
import uuid
from datetime import datetime, timezone
def generate_uuid():
    return str(uuid.uuid4())
class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
