# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:01:46 2013

@authors: David Schoorisse & Mustafa Karaalioglu
"""
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from dbconnection import engine


Base = declarative_base()

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
            

class Answer(Base):
    __tablename__ = 'Answers'
    
    id = Column(Integer, primary_key=True)
    answer = Column(String(96))
    
    def __init__(self, answer):
        self.answer = answer


class AnswerTag(Base):
    __tablename__ = 'AnswerTags'
    
    answer_id = Column(Integer, ForeignKey('Answers.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('Tags.id'), primary_key=True)
    
    def __init__(self, answer_id, tag_id):
        self.answer_id = answer_id
        self.tag_id = tag_id
        
    def __repr__(self):
        return "<AnswerTag('%d', '%d')>" % (self.answer_id, self.tag_id)

Base.metadata.create_all(engine)
