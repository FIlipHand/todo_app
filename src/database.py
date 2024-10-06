from sqlalchemy import ForeignKey, Integer, String, Column, DateTime, Text, Boolean, create_engine, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(Integer, CheckConstraint("priority >= 0 AND priority <= 10"), nullable=False)
    status = Column(String)
    start_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime, nullable=True)
    printed = Column(Boolean, default=False, nullable=False)

    parent_task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)

    parent_task = relationship("Task", remote_side=[id], backref="subtasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title})>"


engine = create_engine("sqlite:///tasks.db", echo=True)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
