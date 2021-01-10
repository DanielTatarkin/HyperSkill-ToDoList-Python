# Write your code here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()
DB_NAME = "todo.db"


# Base Task model for SQLite table
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='empty')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}"


class SqlSession:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{DB_NAME}?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add_task(self, task, date=datetime.today().date()):
        """
        Adds new Task to our SQLite database

        task: Task description string
        date: Task deadline date
        """
        new_row = Task(task=task, deadline=date)
        self.session.add(new_row)
        self.session.commit()

    def delete_task(self, task):
        self.session.delete(task)
        self.session.commit()

    def get_all_tasks(self):
        """
        Retrieves all Tasks from SQLite database
        """
        return self.session.query(Task).order_by(Task.deadline).all()

    def get_today_tasks(self):
        """
        Retrieves all Tasks where deadline is Today
        """
        today = datetime.today()
        return self.session.query(Task).filter(Task.deadline == today.date()).all()

    def get_week_tasks(self):
        """
        Retrieves all Tasks where deadline is within next 7 days
        """
        today = datetime.today().date()
        date_list = [today + timedelta(days=x) for x in range(8)]
        return self.session.query(Task).filter(Task.deadline.in_(date_list)).order_by(Task.deadline).all()

    def get_date_task(self, date):
        """
        Retrieves all Tasks for specific date
        """
        return self.session.query(Task).filter(Task.deadline == date).order_by(Task.deadline).all()

    def get_missed_tasks(self):
        """
        Retrieves all Tasks for specific date
        """
        today = datetime.today()
        return self.session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
