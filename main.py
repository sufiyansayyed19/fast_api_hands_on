from fastapi import FastAPI,status
import json



app = FastAPI()

with open("tasks_db.json","r") as file:
    tasks = json.load(file)


# tasks = [
#     {"id": 1, "title": "Learn FastAPI", "completed": False},
#     {"id": 2, "title": "Build TaskFlow", "completed": False},
# ]


@app.get("/")
def home():
    return {"message": "Welcome to TaskFlow API"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/1")
def get_task():
    return {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    }
    


# @app.post("/tasks")
# def create_task():
#     new_task = {
#         "id": 3,
#         "title": "Learn POST",
#         "completed": False
#     }
#     tasks.append(new_task)

#     return new_task

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task():
    new_task = {
        "id":4,
        "title": "Learn python",
        "completed" : True
    }
    tasks.append(new_task)
    return new_task



@app.post("/task/test")
def create_task4():
    new_task = {
        "id": 4,
        "title": "Testing POST",
        "completed": False
    }
    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id:int):
    for task in tasks:
        if task["id"] == task_id:
            print("Hi ")
            task["title"] =  "Hi there idiot"
            task["completed"] = True
            return task
    return {"message": "task not found"}





@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    print(task_id,"to be deleted")
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return task
    return {"message": "task not found"}


