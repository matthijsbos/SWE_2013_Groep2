from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from dbconnection import engine, session
from base import BaseEntity

Base = declarative_base()

class AnswerModel(Base,BaseEntity):
    __tablename__ = 'answer'
    __table_args__ = {'sqlite_autoincrement' : True}

    text = Column(String)
    questionID = Column(Integer)
    userID = Column(Integer)
    edit = Column(Integer)

    def __repr__(self):
        return self.text + 'Represent'

    def __str__(self):
        return self.text
    
    @staticmethod
    def savereview(questionID,userID,answerText,edit):
        session.add(AnswerModel(questionID=questionID,userID=userID,text=answerText,edit=edit+1))
        session.commit()

    @staticmethod
    def save(questionID,userID,answerText):
        session.add(AnswerModel(questionID=questionID,userID=userID,text=answerText,edit=0))
        session.commit()

Base.metadata.create_all(engine)
