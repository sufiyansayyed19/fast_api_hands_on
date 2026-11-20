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