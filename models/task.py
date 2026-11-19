from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    priority: str = "medium"


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