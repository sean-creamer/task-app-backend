import uuid
from datetime import datetime

from sqlalchemy import Date, Column, Integer, ForeignKey, String, DateTime

from database.base_class import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    assignee = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Integer, nullable=False)
    severity = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=True)
    created_date = Column(DateTime, nullable=False, default=lambda: datetime.now())
