from starlette.status import HTTP_404_NOT_FOUND
from pydantic.deprecated import tools
from fastapi import FastAPI, status
from fastapi import HTTPException
from pydantic import BaseModel
import json
from fastapi import Depends



with open("tasks_db.json", "r") as file:
    tasks = json.load(file)

task_id_counter = 8

app = FastAPI()


def get_message():
    return "Hello from dependency"


@app.get("/dependency")
def dep_demo(message=Depends(get_message)):
    return {
        "message" : message
    }


def get_app_name():
    return "TaskFlow"


def get_environment():
    return "development"

@app.get("/info")
def get_info(app=Depends(get_app_name),env=Depends(get_environment)):
    return {
        "app":app,
        "environment":env
    }

def get_user_role(role: str):
    return role

@app.get("/role")
def role(user_role=Depends(get_user_role)):
    return {"role": user_role}



class Task(BaseModel):
    title:str 
    description:str | None = None
    completed:bool = False
    priority:str = "medium"
    # estimated_hours: int
    # tags: list[str]


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    priority: str

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: str | None = None


# -------------------------
# Topic 2 — CRUD Routes
# -------------------------

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(completed: bool | None = None):
    filtered = []

    if completed is not None:
        for task in tasks:
            if task["completed"] == completed:
                filtered.append(task)
        return filtered

    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def create_task(data: Task):
    global task_id_counter

    task_id_counter += 1

    new_task = {
        "id": task_id_counter,
        "title": data.title,
        "description": data.description,
        "completed": data.completed,
        "priority": data.priority
    }

    tasks.append(new_task)

    return new_task


@app.put(
    "/tasks/{task_id}",
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


@app.patch(
    "/tasks/{task_id}",
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


@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )



