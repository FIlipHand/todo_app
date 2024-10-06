from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.tasks_api import create_task, close_task, create_subtask, update_priority, update_status, get_task, get_all_tasks
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



@app.post("/tasks/", response_model=TaskResponse)
def app_create_task(task: TaskBase):
    new_task_id, error = create_task(task.title, task.description, task.priority, task.status)
    if error is not None:
        raise HTTPException(status_code=400, detail=error)
    return {"id": new_task_id, "title": task.title}


@app.get("/tasks/", response_model=List[FullTask])
def app_get_all_tasks():
    tasks, error = get_all_tasks()
    if error is not None:
        raise HTTPException(status_code=400, detail=error)
    return tasks

    
