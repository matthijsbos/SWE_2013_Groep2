from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from dbconnection import engine, session
from datetime import datetime


class BaseEntity(object):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def get_all(cls):
        return session.query(cls).filter().all()

    @classmethod
    def by_id(cls, id):
        try:
            return session.query(cls).filter(cls.id == id).one()
        except:
            return None

    @classmethod
    def remove_by_id(cls, id):
        entry = cls.by_id(id)
        if entry == None:
            return
        session.delete(entry)
        session.commit()

    @classmethod
    def by_ids(cls, ids):
        if not ids:
            return []
        return session.query(cls).filter(cls.id.in_(ids)).all()

    @classmethod
    def get_filtered(cls, **kws):
        if len(kws) > 0:
            return session.query(cls).filter_by(**kws).all()
        return cls.get_all()
