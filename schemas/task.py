from datetime import date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class Severity(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2


class TaskCreate(BaseModel):
    title: str
    description: str
    assignee: Optional[int] = None
    status: Status
    severity: Severity
    priority: Priority
    due_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee: Optional[int] = None
    status: Optional[Status] = None
    severity: Optional[Severity] = None
    priority: Optional[Priority] = None
    due_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class TaskCreateResponse(BaseModel):
    id: str
    title: str
    description: str
    assignee: Optional[int]
    status: Status
    severity: Severity
    priority: Priority
    due_date: Optional[date]

    model_config = ConfigDict(from_attributes=True)


TaskUpdateResponse = TaskCreateResponse


class TaskGetResponse(BaseModel):
    id: str
    title: str
    description: str
    assignee_name: Optional[str]
    status: Status
    severity: Severity
    priority: Priority
    due_date: Optional[date]

    model_config = ConfigDict(from_attributes=True)

class Pagination(BaseModel):
    total: int
    more: bool
    offset: int
    limit: int

class TasksGetResponse(BaseModel):
    tasks: List[TaskGetResponse]
    pagination: Pagination
    model_config = ConfigDict(from_attributes=True)

class TaskRecommendSeverity(BaseModel):
    title: str
    description: str


