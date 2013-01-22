from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer
from dbconnection import engine, session, Base
from basemodel import BaseEntity


class Question(Base, BaseEntity):
    __tablename__ = 'questions'

    teacher_id = Column(String)
    course_id = Column(String)
    question = Column(String)
    available = Column(Boolean)
    time = Column(Integer)

    def __init__(self, teacher_id, course_id, question, available, time):
        self.teacher_id = teacher_id
        self.course_id = course_id
        self.question = question
        self.available = available
        self.time = time

    def __repr__(self):
        return "<Question ('%s','%s','%s')>" % (self.teacher_id,
                                                self.question,
                                                self.available)

    @classmethod
    def by_course_id(cls, course_id):
        return session.query(cls).filter(cls.course_id == course_id).all()

    @classmethod
    def toggle_available(cls, q_id):
        question = Question.by_id(q_id)
        question.available = not question.available
        session.commit()
        return question.available

