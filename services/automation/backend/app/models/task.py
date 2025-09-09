from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    steps = Column(JSON, nullable=True)  # List of automation steps
    prerequisites = Column(JSON, nullable=True)  # File requirements, etc.
    status = Column(String(50), default="draft")  # draft, ready, running, completed, failed
    script_path = Column(String(255), nullable=True) # Path to the automation script
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    executions = relationship("Execution", back_populates="task", cascade="all, delete-orphan")
    files = relationship("File", back_populates="task", cascade="all, delete-orphan")

# Pydantic models for API
class TaskStep(BaseModel):
    action: str  # navigate, click, type, wait, select, screenshot, interactive_pause
    target: Optional[str] = None  # CSS selector, URL, etc.
    value: Optional[str] = None  # Text to type, option to select, etc.
    description: Optional[str] = None

class TaskPrerequisite(BaseModel):
    type: str  # file_upload, environment_variable, etc.
    name: str
    description: Optional[str] = None
    required: bool = True

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    steps: Optional[List[TaskStep]] = None # Make steps optional
    prerequisites: Optional[List[TaskPrerequisite]] = None
    script_path: Optional[str] = None # Add script_path

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[List[TaskStep]] = None
    prerequisites: Optional[List[TaskPrerequisite]] = None
    status: Optional[str] = None
    script_path: Optional[str] = None # Add script_path

class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    steps: Optional[List[TaskStep]] # Make steps optional
    prerequisites: Optional[List[TaskPrerequisite]]
    status: str
    script_path: Optional[str] # Add script_path
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
