from fastapi import APIRouter, status, HTTPException
from models.task import Task, TaskResponse,TaskUpdate
from data.tasks import tasks

router = APIRouter(prefix="/tasks")


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