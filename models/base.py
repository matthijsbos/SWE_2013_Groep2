from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from dbconnection import engine,session
from datetime import datetime

Base = declarative_base()

class BaseEntity(object):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    @classmethod
    def get_all(cls):
        return session.query(cls).filter().all()

    @classmethod
    def by_id(cls, id):
        return session.query(cls).filter(self.id == id).one()


    @classmethod
    def by_ids(cls, ids):
        if not ids:
            return []

        return session.query(cls).filter(cls.id.in_(ids)).all()
