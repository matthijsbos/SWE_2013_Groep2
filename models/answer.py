from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from dbconnection import engine, session

Base = declarative_base()

class AnswerModel(Base):
    __tablename__ = 'answer'
    __table_args__ = {'sqlite_autoincrement' : True}

    answerID = Column(Integer,primary_key=True)
    text = Column(String)
    questionID = Column(Integer)
    userID = Column(Integer)

    def __repr__(self):
        return self.text + 'Represent'

    def __str__(self):
        return self.text

    @staticmethod
    def getall():
        return [x for x in session.query(AnswerModel)]

    @staticmethod
    def save(questionID,userID,answerText):
        session.add(AnswerModel(questionID=questionID,userID=userID,text=answerText))
        session.commit()

Base.metadata.create_all(engine)
