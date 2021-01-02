# Write your code here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime

sql = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='empty')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class SqlSession(sessionmaker):
    def __init__(self, **kw):
        super().__init__(**kw, bind=sql)
        self.session = self()

    def add_task(self, task):
        # , deadline=datetime.strptime(deadline, '%m-%d-%Y').date()
        new_row = Table(task=task)
        self.session.add(new_row)
        self.session.commit()

    def query(self):
        return self.session.query(Table).all()




Base.metadata.create_all(sql)