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

# @router.get("/db-test")
# def db_test(db: Session = Depends(get_db)):
#     statement = select(TaskDB)
#     result = db.execute(statement)
#     # return {"result": result.scalar().all()}
#     return result.scalars().all()

@router.get("/db-tasks")
def get_db_tasks(db: Session = Depends(get_db)):
    statement = select(TaskDB)

    result = db.execute(statement)

    tasks = result.scalars().all()

    return tasks

@router.post("/db-user")
def create_db_user(db: Session = Depends(get_db)):
    user = UserDB(
        email="sufiyan@example.com"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



@router.post("/db-test")
def create_db_test(db: Session = Depends(get_db)):
    task = TaskDB(
        title="Learn SQLAlchemy",
        description="Practice SQLAlchemy CRUD",
        priority="high",
        user_id=1
    )

    db.add(task)
    db.commit()

    return {"message": "Task created"}


@router.put("/db-test/{task_id}")
def update_db_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(TaskDB, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.completed = True
    task.priority = "high"

    db.commit()
    db.refresh(task)

    return task


@router.delete("/db-test/{task_id}")
def delete_db_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(TaskDB, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


























@router.get("", response_model=list[TaskResponse])
def get_tasks(completed: bool | None = None):
    filtered = []

    if completed is not None:
        for task in tasks:
            if task["completed"] == completed:
                filtered.append(task)
        return filtered

    return tasks


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def create_task(data: Task):
    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "title": data.title,
        "description": data.description,
        "completed": data.completed,
        "priority": data.priority
    }

    tasks.append(new_task)

    return new_task


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(task_id: int, data: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.title
            task["description"] = data.description
            task["completed"] = data.completed
            task["priority"] = data.priority

            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task_part(task_id: int, data: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:

            if data.title is not None:
                task["title"] = data.title

            if data.description is not None:
                task["description"] = data.description

            if data.completed is not None:
                task["completed"] = data.completed

            if data.priority is not None:
                task["priority"] = data.priority

            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )   


@router.delete(
    "/{task_id}",
    response_model=TaskResponse
)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )