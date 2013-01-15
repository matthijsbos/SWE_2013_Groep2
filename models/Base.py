from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class BaseEntity(object):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    @classmethod
    def get_all(self, session):
        return session.query(self).filter().all()


    @classmethod
    def by_id(self, session, id):
        return session.query(self).filter(self.id == id).one()


    @classmethod
    def by_ids(self, sesion, ids):
        if not ids:
            return []

        return session.query(self).filter(self.id.in_(ids)).all()
