from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean
from dbconnection import engine, session
from Base import BaseEntity

Base = declarative_base()

class Question(Base, BaseEntity):
    __tablename__ = 'questions'

    teacher_id = Column(String)
    course_id = COlumn(String)
    question = Column(String)
    available = Column(Boolean)


    def __init__(self, teacher_id, course_id, question, available):
        self.teacher_id = teacher_id
        self.course_id = course_id
        self.question = question
        self.available = available

    def __repr__(self):
        return "<Question ('%s','%s','%s')>" % (self.teacher_id,
                                                self.question,
                                                self.available)


Base.metadata.create_all(engine)
