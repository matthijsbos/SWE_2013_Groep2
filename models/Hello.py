from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from dbconnection import engine

Base = declarative_base()

class Model(Base):
    __tablename__ = 'helloworld'

    id = Column(Integer, primary_key=True)
    text = Column(String)

    def __init__(self, text, modelname):
        self.text = text

    def __repr__(self):
        return self.text

    @staticmethod
    def getall():
        return ['Hello','World','!']


Base.metadata.create_all(engine)
