# Write your code here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()
DB_NAME = "todo.db"


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='empty')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task}"


class SqlSession:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{DB_NAME}?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add_task(self, task):
        new_row = Table(task=task)
        self.session.add(new_row)
        self.session.commit()

    def get_tasks(self):
        return self.session.query(Table).all()
