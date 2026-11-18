from starlette.status import HTTP_404_NOT_FOUND
from pydantic.deprecated import tools
from fastapi import FastAPI, status
from fastapi import HTTPException
from pydantic import BaseModel
import json

with open("tasks_db.json", "r") as file:
    tasks = json.load(file)

task_id_counter = 8

app = FastAPI()


class Task(BaseModel):
    title:str 
    description:str | None = None
    completed:bool = False
    priority:str = "Medium"
    # estimated_hours: int
    # tags: list[str]


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    priority: str




# -------------------------
# Topic 2 — CRUD Routes
# -------------------------

@app.get("/tasks",response_model=list[TaskResponse])
def get_tasks(completed:bool|None = None):
    filtered = list()
    if (completed == True or completed == False):
        for task in tasks:
            if task["completed"] == completed:
                filtered.append(task)
        return filtered
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
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


# @app.get("/tasks/{task_id}")
# def get_task(task_id: int):
#     for task in tasks:
#         if task["id"] == task_id:
#             return task

#     return {"message": "task not found"}


@app.get("/tasks/{task_get}", response_model=TaskResponse)
def get_tasks(task_id:int):
    for task in tasks:
          if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

# # @app.put("/tasks/{task_id}")
# def update_task(task_id: int):
#     for task in tasks:
#         if task["id"] == task_id:
#             task["title"] = "I am updated"
#             task["completed"] = True

#             return task

#     return {"message": "task not found"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.title
            task["description"] = data.description
            task["completed"] = data.completed
            task["priority"] = data.priority

            return task

    return {"message": "task not found"}

@app.patch("/tasks/{task_id}")
def update_task_part(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = "I am updated partially"

            return task

    return {"message": "task not found"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return task

    return {"message": "task not found"}


# -------------------------
# Topic 3 — Parameter Practice
# -------------------------

# 3.4 Multiple Path Parameters

@app.get("/users/{user_id}/tasks/{task_id}")
def get_user_task(user_id: int, task_id: int):
    return {
        "user_id": user_id,
        "task_id": task_id
    }


# 3.9 Path + Query Parameters

@app.get("/users/{user_id}/tasks")
def get_user_tasks(
    user_id: int,
    completed: bool | None = None
):
    return {
        "user_id": user_id,
        "completed": completed
    }

# temp post
@app.post("/practice")
def practice(data: Task):
    return data