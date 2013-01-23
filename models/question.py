from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer,DateTime
from dbconnection import engine, session, Base
from basemodel import BaseEntity
from datetime import datetime


class Question(Base, BaseEntity):
    __tablename__ = 'questions'

    teacher_id = Column(String)
    course_id = Column(String)
    question = Column(String)
    available = Column(Boolean)
    time = Column(Integer)
    activate_time = Column(DateTime,nullable=True)
    
    comment = Column(Boolean)
    tags = Column(Boolean)
    rating = Column(Boolean)

    def __init__(self, teacher_id, course_id, question, available,time, comment, tags, rating, activate_time = None):
        self.teacher_id = teacher_id
        self.course_id = course_id
        self.question = question
        self.available = available
        
        self.comment = comment
        self.tags = tags
        self.rating = rating

        if(available and self.activate_time is None):
            self.activate_time = datetime.now()
        else:
            self.activate_time = activate_time
        self.time = time

    def __repr__(self):
        return "<Question ('%s','%s','%s','%s','%s','%s','%s')>" % (self.teacher_id,
                                                self.question,
                                                self.available,
                                                self.time,
                                                self.comment,
                                                self.tags,
                                                self.rating)

    @classmethod
    def by_course_id(cls, course_id):
        return session.query(cls).filter(cls.course_id == course_id).all()

    @classmethod
    def toggle_available(cls, q_id):
        question = Question.by_id(q_id)
        question.available = not question.available

        dt = None
        if question.available:
            dt = datetime.now()

        question.activate_time = dt
        session.commit()
        return question.available

Base.metadata.create_all(engine)
