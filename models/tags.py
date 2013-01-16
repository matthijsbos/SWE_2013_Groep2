# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:01:46 2013

@authors: David Schoorisse & Mustafa Karaalioglu
"""
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from dbconnection import engine, session
from models.answer import AnswerModel, Base

class Tag(Base):
    __tablename__ = 'Tags'
    
    id = Column(Integer, Sequence('id'), primary_key=True, unique=True)
    name = Column(String(32), unique=True)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        if self.id is None:
            return "<Tag('None', '%s')>" % (self.name)
        else:
            return "<Tag('%d', '%s')>" % (self.id, self.name)
            
    @staticmethod 
    def add_tag(name):
        if session.query(Tag.name).filter(Tag.name==name).first() is None:
            session.add(Tag(name))
            session.commit()

    @staticmethod 
    def remove_tag(tag_id):
        for tag in session.query(Tag).filter(Tag.id==tag_id):
            session.delete(tag)


class AnswerTag(Base):
    __tablename__ = 'AnswerTags'
    
    answer_id = Column(Integer, ForeignKey('answer.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('Tags.id'), primary_key=True)
    
    def __init__(self, answer_id, tag_id):
        self.answer_id = answer_id
        self.tag_id = tag_id
        
    def __repr__(self):
        return "<AnswerTag('%d', '%d')>" % (self.answer_id, self.tag_id)

Base.metadata.create_all(engine)
