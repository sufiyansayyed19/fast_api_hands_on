# from fastapi import FastAPI

# app = FastAPI()

# @app.post("/tasks/{task_id}")
# def update_task(task_id: int):
#     for task in tasks:
#         if task["id"] == task_id:
#             task["title"] = "Learn FastAPI properly"
#             task["Completed"] =  True
#             return task
#     return {"message": "Task not found"}