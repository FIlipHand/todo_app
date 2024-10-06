from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.tasks_api import create_task, close_task, create_subtask, update_priority, update_status, get_task
from typing import Optional

app = FastAPI()


class TaskBase(BaseModel):
    title: str
    description: str
    priority: int
    status: Optional[str] = None
    parent_id: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str


@app.post("/tasks/", response_model=TaskResponse)
def app_create_task(task: TaskBase):
    new_task_id = create_task(task.title, task.description, task.priority, task.status)
    return {"id": new_task_id, "title": task.title}
