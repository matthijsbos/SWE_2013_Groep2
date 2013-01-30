from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer,DateTime
from dbconnection import engine, session, Base
from basemodel import BaseEntity
from datetime import datetime, timedelta


class Question(Base, BaseEntity):
    __tablename__ = 'questions'

    user_id = Column(String)
    course_id = Column(String)
    question = Column(String)

    # we don't need to have seperate toggle_methods,
    # just use if Question.xavailble: bla bla
    _answerable = Column(Boolean)
    _reviewable = Column(Boolean)
    _archived = Column(Boolean)
    state = Column(String)
    time = Column(Integer)
    activate_time = Column(DateTime,nullable=True)
    
    comment = Column(Boolean)
    tags = Column(Boolean)
    rating = Column(Boolean)

    def __init__(self, user_id, course_id, question, answerable, time, comment, tags, rating):
        self.user_id = user_id
        self.course_id = course_id
        self.question = question
        
        self.state = 'States'
        self.comment = comment
        self.tags = tags
        self.rating = rating

        if(answerable):
            self.activate_time = datetime.now()
            self.state = 'Answerable'
        else:
            self.activate_time = None

        self.time = time
        self.answerable = answerable
        self.reviewable = False
        self.archived = False

    def __repr__(self):
        return "<Question ('%s','%s','%s', '%s')>" % (self.user_id,
                                                self.question,
                                                self.answerable,
                                                self.reviewable)

    def get_time_left(self):
        if self.time == 0 or self.activate_time == None:
            time_remaining = 0
        else:
            time_remaining = datetime.now() - (self.activate_time +
                    timedelta(seconds=self.time))
            time_remaining = time_remaining.seconds + time_remaining.days*86400
            time_remaining = -time_remaining
            
        return time_remaining
    
    """
    Yay properties
    """
    @property
    def answerable(self):
         return self._answerable

    @answerable.setter
    def answerable(self, value):
         self._answerable = value
         session.add(self)
         session.commit()

    @property
    def reviewable(self):
         return self._reviewable

    @reviewable.setter
    def reviewable(self, value):
         self._reviewable = value
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


class UserQuestion(Base, BaseEntity):
    __tablename__ = "UserQuestions"
    
    user_id = Column(String)
    text = Column(String)
    
    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
        
    @classmethod
    def add(cls, user_id, text):
        session.add(cls(user_id, text))
        session.commit()
        
    @classmethod
    def time_since_last(cls, user_id):
        created = session.query(cls.created).filter(
            cls.user_id == user_id).order_by(cls.id.desc()).first()
        
        if created is None:
            return None
            
        dt = datetime.now() - created[0]
        return dt.seconds + dt.days*86400
        
        
Base.metadata.create_all(engine)
