# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:01:46 2013

@authors: David Schoorisse & Mustafa Karaalioglu
"""
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from dbconnection import engine, session, Base
from models.answer import AnswerModel
from basemodel import BaseEntity

#A way to serialize SQLalchemy results
#Source: http://piotr.banaszkiewicz.org/blog/2012/06/30/serialize-sqlalchemy-results-into-json/
from collections import OrderedDict
class DictSerializable(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

class Tag(Base, BaseEntity):
    __tablename__ = 'Tags'

    name = Column(String(32), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.id is None:
            return "<Tag('None', '%s')>" % (self.name)
        else:
            return "<Tag('%d', '%s')>" % (self.id, self.name)

    @staticmethod
    def get_all():
        return session.query(Tag).filter().all()

    @staticmethod
    def add_tag(name):
        if session.query(Tag.name).filter(Tag.name == name).first() is None:
            session.add(Tag(name))
            session.commit()
            
    @staticmethod
    def remove_tag(tag_id):
        for tag in session.query(Tag).filter(Tag.id == tag_id):
            session.delete(tag)
            session.commit()


class AnswerTag(Base):
    __tablename__ = 'AnswerTags'
    
    answer_id = Column(Integer, ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('Tags.id', ondelete='CASCADE'), primary_key=True)

    def __init__(self, answer_id, tag_id):
        self.answer_id = answer_id
        self.tag_id = tag_id

    def __repr__(self):
        return "<AnswerTag('%d', '%d')>" % (self.answer_id, self.tag_id)
        
    @staticmethod
    def get_all():
        return session.query(AnswerTag).filter().all()

    @staticmethod
    def add_answertag(aid, tid):
        if session.query(AnswerTag).filter(
                AnswerTag.answer_id==aid,
                AnswerTag.tag_id==tid).first() is None:
            session.add(AnswerTag(aid, tid))
            session.commit()
                
    @staticmethod
    def remove(answer_id, tag_id):
        for at in session.query(AnswerTag).filter(
                AnswerTag.answer_id==answer_id,
                AnswerTag.tag_id==tag_id):
            session.delete(at)
            session.commit()
            

    @staticmethod
    def get_tag_ids(answerID):
        tlist = session.query(AnswerTag.tag_id).filter(
                AnswerTag.answer_id==answerID).all()
        map(list, tlist)
        endlist = []
        for x in tlist:
            endlist.append(x[0])
        return endlist 

Base.metadata.create_all(engine)
