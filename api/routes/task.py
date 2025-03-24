import json
from datetime import date
from typing import Optional
from uuid import UUID

import openai
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import security
from config import Config
from database.db import get_db
from models.task import Task
from models.users import User
from schemas.task import TaskCreate, TaskCreateResponse, TaskUpdate, TaskUpdateResponse, TasksGetResponse, \
    TaskRecommendSeverity, Status

router = APIRouter()

if not Config.OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in your .env file or environment variables.")

openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)


@router.post("/task", response_model=TaskCreateResponse)
def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        _: str = Depends(security.token_required),
):
    db_task = Task(
        title=task.title,
        description=task.description,
        assignee=task.assignee,
        status=task.status.value,
        severity=task.severity.value,
        priority=task.priority.value,
        due_date=task.due_date,
    )
    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    # TODO: Proper error handling
    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="Task not valid")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")


@router.put("/task/{task_id}", response_model=TaskUpdateResponse)
def update_task(
        task_id: str,
        task: TaskUpdate,
        db: Session = Depends(get_db),
        _: str = Depends(security.token_required)
):
    try:
        task_id = UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task id")
    db_task = db.query(Task).filter(Task.id == str(task_id)).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title:
        db_task.title = task.title
    if task.description:
        db_task.description = task.description
    if task.assignee:
        db_task.assignee = None if task.assignee == -1 else task.assignee
    if task.status:
        db_task.status = task.status.value
    if task.severity:
        db_task.severity = task.severity.value
    if task.priority:
        db_task.priority = task.priority.value
    if task.due_date:
        db_task.due_date = task.due_date

    try:
        db.commit()
        db.refresh(db_task)
        return db_task

    # TODO: Proper error handling
    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="Task update failed due to integrity constraints")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")


@router.get("/tasks", response_model=TasksGetResponse)
def get_tasks(
        db: Session = Depends(get_db),
        _: str = Depends(security.token_required),
        status: Optional[int] = Query(None, description="Filter by task status"),
        assignee: Optional[int] = Query(None, description="Filter by assignee id"),
        offset: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100, description="Limit the number of results"),
):
    query = (
        db.query(
            Task.id,
            Task.title,
            Task.description,
            User.username.label("assignee_name"),  # Fetch username from users table
            Task.status,
            Task.severity,
            Task.priority,
            Task.due_date
        )
        .outerjoin(User, Task.assignee == User.id)  # LEFT JOIN to include tasks with no assignee
    )

    # Always exclude "Done" tasks (status = 1) unless explicitly filtered by status
    if status is None:
        query = query.filter(Task.status != 2)  # Exclude "Done" tasks
    elif status is not None:
        query = query.filter(Task.status == status)

    if assignee == -1:
        query = query.filter(Task.assignee.is_(None))
    elif assignee is not None:
        query = query.filter(Task.assignee == assignee)

    total_count = query.count()

    query = query.order_by(
        Task.due_date.asc().nullslast(),
        Task.priority.desc()
    )

    tasks = query.offset(offset).limit(limit).all()

    more = (offset + limit) < total_count

    response = {
        "tasks": [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "assignee_name": task.assignee_name or "Unassigned",
                "status": task.status,
                "severity": task.severity,
                "priority": task.priority,
                "due_date": task.due_date
            } for task in tasks
        ],
        "pagination": {
            "total": total_count,
            "more": more,
            "offset": offset,
            "limit": limit
        }
    }

    return response


@router.post("/task/recommend-fields")
def recommend_severity_priority(
        task: TaskRecommendSeverity,
        _: str = Depends(security.token_required)
):
    prompt = (
        "Based on the following task title and description, suggest a severity level (Low, Medium, High) "
        "and a priority level (Low, Medium, High). \n"
        f"Title: {task.title}\n"
        f"Description: {task.description}\n\n"
        "Respond in this exact format "
        "{'severity': <Severity Level you recommend (from the options provided earlier), 'priority': <Priority Level you recommend>} \n"
        "Return in valid JSON that I can simply parse without extra steps."
    )

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,  # Allow enough space for both values
        )

        ai_response = response.choices[0].message.content.strip()

        # Extract severity and priority using basic parsing
        severity = None
        priority = None

        obj = json.loads(ai_response)
        severity = obj['severity']
        priority = obj['priority']

        if not severity or not priority:
            raise ValueError("Invalid AI response format")

        return {"severity": severity, "priority": priority}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/open-count", response_model=dict)
def get_open_tasks_count(
        db: Session = Depends(get_db),
        _: str = Depends(security.token_required),
        assignee: Optional[int] = Query(None, description="Filter by assignee id"),
        due_date: Optional[date] = Query(None, description="Filter by due date (YYYY-MM-DD)")
):
    try:
        query = db.query(Task).filter(Task.status != Status.DONE.value)

        if assignee == -1:
            query = query.filter(Task.assignee.is_(None))
        elif assignee is not None:
            query = query.filter(Task.assignee == assignee)

        if due_date is not None:
            query = query.filter(Task.due_date == due_date)

        open_count = query.count()

        return {"open_count": open_count}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/percentage-complete", response_model=dict)
def get_task_summaries(
        db: Session = Depends(get_db),
        _: str = Depends(security.token_required)
):
    try:
        total_tasks = db.query(Task).count()
        done_tasks = db.query(Task).filter(Task.status == Status.DONE.value).count()

        return {
            "total": total_tasks,
            "done": done_tasks
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch task summaries: {str(e)}")


@router.post("/task/suggest-new", response_model=dict)
def get_next_task_suggestion(
        request: Request,
        db: Session = Depends(get_db),
        _: str = Depends(security.token_required),
):
    try:
        current_user = security.get_current_user(request.headers["Authorization"])
        tasks = db.query(Task).filter(Task.assignee == current_user).order_by(Task.created_date.desc()).limit(5).all()

        prompt = (
            "Based on the following task descriptions, generate a new task description for someone to complete:"
        )

        for task in tasks:
            prompt += f'\n{task.description}'

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,  # Allow enough space for both values
        )
        description = response.choices[0].message.content.strip()
        return {'newTaskDescription': description}
    except Exception as e:
        print(e)
