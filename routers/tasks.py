from fastapi import APIRouter, status, HTTPException, Depends
from models.task import Task, TaskResponse,TaskUpdate
from data.tasks import tasks
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from database.dependency import get_db
from models.task_db import TaskDB
from models.user_db import UserDB



router = APIRouter(
    prefix="/tasks",
    tags= ["Tasks"])

@router.get("")
def get_tasks(
    completed: bool | None = None,
    db: Session = Depends(get_db)
):
    statement = select(TaskDB)

    if completed is not None:
        statement = statement.where(
            TaskDB.completed == completed
        )

    result = db.execute(statement)

    tasks = result.scalars().all()

    return tasks


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    data: Task,
    db: Session = Depends(get_db)
):
    task = TaskDB(
        title=data.title,
        description=data.description,
        completed=data.completed,
        priority=data.priority,
        user_id=1
    )

    db.add(task)

    try:
        db.commit()
        db.refresh(task)
    except:
        db.rollback()
        raise

    return task

@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    data: Task,
    db: Session = Depends(get_db)
):
    task = db.get(TaskDB, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.title = data.title
    task.description = data.description
    task.completed = data.completed
    task.priority = data.priority

    try:
        db.commit()
        db.refresh(task)
    except:
        db.rollback()
        raise

    return task