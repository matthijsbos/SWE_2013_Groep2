from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer,DateTime
from dbconnection import engine, session, Base
from basemodel import BaseEntity
from datetime import datetime


class Question(Base, BaseEntity):
    __tablename__ = 'questions'

    user_id = Column(String)
    course_id = Column(String)
    question = Column(String)

    # we don't need to have seperate toggle_methods,
    # just use if Question.xavailble: bla bla
    _answeravailable = Column(Boolean)
    _reviewavailable = Column(Boolean)
    _archived = Column(Boolean)
    time = Column(Integer)
    activate_time = Column(DateTime,nullable=True)
    
    comment = Column(Boolean)
    tags = Column(Boolean)
    rating = Column(Boolean)

    def __init__(self, user_id, course_id, question, available, time):
        self.user_id = user_id
        self.course_id = course_id
        self.question = question
        self.answeravailable = available
        self.time = time
        self.answeravailable = False
        self.reviewavailable = False
        self.archived = False

    def __repr__(self):
        return "<Question ('%s','%s','%s', '%s')>" % (self.user_id,
                                                self.question,
                                                self.answeravailable,
                                                self.reviewavailable)

    """
    Yay properties
    """
    @property
    def answeravailable(self):
         return self._answeravailable

    @answeravailable.setter
    def answeravailable(self, value):
         self._answeravailable = value
         session.add(self)
         session.commit()

    @property
    def reviewavailable(self):
         return self._reviewavailable

    @reviewavailable.setter
    def reviewavailable(self, value):
         self._reviewavailable = value
         session.add(self)
         session.commit()

    @property
    def archived(self):
         return self._archived

    @archived.setter
    def archived(self, value):
         self._archived = value
         session.add(self)
         session.commit()

    @classmethod
    def by_course_id(cls, course_id):
        return session.query(cls).filter(cls.course_id == course_id).all()

Base.metadata.create_all(engine)
