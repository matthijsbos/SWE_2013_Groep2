from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from dbconnection import engine, session

Base = declarative_base()

class Model(Base):
    __tablename__ = 'helloworld'

    text = Column(String, primary_key=True)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

    @staticmethod
    def getall():
        # get a list with strings
        strlist = []
        for model in session.query(Model):
            strlist.append(model.text)
        return strlist

Base.metadata.create_all(engine)
