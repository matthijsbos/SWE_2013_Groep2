from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from dbconnection import engine, session
from datetime import datetime

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    teacher_id = Column(String)
    question = Column(String)
    available = Column(Boolean)


    def __init__(self, teacher_id, question, available):
        self.teacher_id = teacher_id
        self.question = question
        self.available = available

    def __repr__(self):
        return "<Question ('%s','%s','%s')>" % (self.question,
                                                self.teacher_id,
                                                self.available)

    @staticmethod
    def by_id(id):
        return session.query(Question).filter(Question.id == id).one()


Base.metadata.create_all(engine)
