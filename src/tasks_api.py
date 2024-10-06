from typing import List
from src.database import SessionLocal, Task
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


def create_task(title: str, description: str, priority: int, status: str = None):
    error, new_id = None, None
    if status is None:
        status = "To Do"
    try:
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
            session.refresh(new_task)
            new_id = new_task.id
    except SQLAlchemyError as e:
        error = e
    finally:
        return new_id, error


def create_subtask(task_parent_id: int, title: str, description: str, priority: int, status: str = None):
    if status is None:
        status = "To Do"
    new_id, error = None, None
    try:
        with SessionLocal() as session:
            parent_task = session.query(Task).filter(Task.id == task_parent_id).first()
            if parent_task is None:
                print("No such parent task!")
                return Exception()
            if parent_task.close_date is not None:
                print("Cannot add subtask to closed task!")
                return Exception()
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
            session.refresh(sub_task)
            new_id = sub_task.id
    except SQLAlchemyError as e:
        error = e
    finally:
        return new_id, error


def close_task(task_id: int):
    closed_id, error = None, None
    try:
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                print(f"No task with id {task_id}")
                return Exception()
            task.close_date = datetime.now()
            session.commit()
            closed_id = task.id
    except SQLAlchemyError as e:
        error = e
    finally:
        return closed_id, error


def update_status(task_id: int, new_status: str):
    updated_id, error = None, None
    try:
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task.close_date is not None:
                print("Cannot modify closed task!")
                return None, Exception()
            task.status = new_status
            session.commit()
            updated_id = task.id
    except SQLAlchemyError as e:
        error = e
    finally:
        return updated_id, error


def update_priority(task_id: int, new_priority: int):
    updated_id, error = None, None
    try:
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task.close_date is not None:
                print("Cannot modify closed task!")
                return None, Exception()
            task.priority = new_priority
            session.commit()
            updated_id = task.id
    except SQLAlchemyError as e:
        error = e
    finally:
        return updated_id, error


def get_task(task_id: int) -> Task:
    task, error = None, None
    try:
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
    except SQLAlchemyError as e:
        error = e
    return task, error


def get_all_tasks() -> List[Task]:
    tasks, error = None, None
    try:
        with SessionLocal() as session:
            tasks = session.query(Task).all()
    except SQLAlchemyError as e:
        error = e
    finally:
        return tasks, error
