from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from dbconnection import engine

Base = declarative_base()

class Hello(Base):
    __tablename__ = 'helloworld'

    id = Column(Integer, primary_key=True)
    text = Column(String)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

Base.metadata.create_all(engine)
