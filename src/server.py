from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.tasks_api import (
    create_task,
    close_task,
    create_subtask,
    update_priority,
    update_status,
    get_task,
    get_all_tasks,
)
from typing import Optional, List
from datetime import datetime

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


class FullTask(TaskBase):
    id: int
    printed: bool
    start_date: datetime
    close_date: Optional[datetime]


class TaskId(BaseModel):
    id: int


@app.post("/tasks/create_task", response_model=TaskResponse)
def app_create_task(task: TaskBase):
    new_task_id, error = create_task(task.title, task.description, task.priority, task.status)
    if error is not None:
        raise HTTPException(status_code=400, detail=str(error))
    return {"id": new_task_id, "title": task.title}


@app.get("/tasks/get_all_tasks", response_model=List[FullTask])
def app_get_all_tasks():
    tasks, error = get_all_tasks()
    if error is not None:
        raise HTTPException(status_code=400, detail=str(error))
    return tasks


@app.get("/tasks/close_task", response_model=TaskId)
def app_close_task(task: TaskId):
    task_id, error = close_task(task_id=task.id)
    if error is not None:
        raise HTTPException(status_code=400, detail=str(error))
    return task_id


@app.get("/tasks/create_subtask")
def app_create_subtask():
    subtask_id, error = create_subtask()
    if error is not None:
        raise HTTPException(status_code=400, detail=str(error))
    return subtask_id
