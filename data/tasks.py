import json

with open("tasks_db.json", "r") as file:
    tasks = json.load(file)

task_id_counter = 8