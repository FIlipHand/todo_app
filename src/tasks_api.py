from typing import List
from src.database import SessionLocal, Task
from datetime import datetime


def create_task(title: str, description: str, priority: int, status: str = None) -> int:
    if status is None:
        status = "To Do"
    with SessionLocal() as session:
        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status,
            start_date=datetime.now(),
        )
        session.add(new_task)
        session.commit()
        return new_task.id


def create_subtask(task_parent_id: int, title: str, description: str, priority: int, status: str = None):
    if status is None:
        status = "To Do"
    with SessionLocal() as session:
        parent_task = session.query(Task).filter(Task.id == task_parent_id).first()
        if parent_task is None:
            print("No such parent task!")
            return
        if parent_task.close_date is not None:
            print("Cannot add subtask to closed task!")
            return
        sub_task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status,
            start_date=datetime.now(),
            parent_task_id=task_parent_id,
        )
        session.add(sub_task)
        session.commit()


def close_task(task_id: int):
    with SessionLocal() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            print(f"No task with id {task_id}")
            return
        task.close_date = datetime.now()
        session.commit()


def update_status(task_id: int, new_status: str):
    with SessionLocal() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task.close_date is not None:
            print("Cannot modify closed task!")
            return
        task.status = new_status
        session.commit()


def update_priority(task_id: int, new_priority: int):
    with SessionLocal() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task.close_date is not None:
            print("Cannot modify closed task!")
            return
        task.priority = new_priority
        session.commit()


def get_task(task_id: int) -> Task:
    with SessionLocal() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
    return task


def get_all_tasks() -> List[Task]:
    with SessionLocal() as session:
        tasks = session.query(Task).all()
        return tasks
