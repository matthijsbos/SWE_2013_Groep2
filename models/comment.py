# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:37:35 2013

@author: Robin van Rijn & Mustafa Karaalioglu
"""

from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from dbconnection import engine, session, Base
from models.answer import AnswerModel
from basemodel import BaseEntity


class Comment(Base, BaseEntity):
    __tablename__ = 'Comments'
    
    answer_id = Column(Integer, ForeignKey('answer.id', ondelete='CASCADE'))
    user_id = Column(String)
    text = Column(String)
    
    def __init__(self, answer_id, user_id, text):
        self.answer_id = answer_id
        self.user_id = user_id
        self.text = text
        
    def __repr__(self):
        return "<Comment(aid='%d', uid='%s', '%s')" % (self.answer_id,
            self.user_id, self.text)
    
    @staticmethod        
    def add(answer_id, user_id, text):
        if session.query(Comment).filter(Comment.answer_id == answer_id,
                Comment.user_id == user_id).first() is not None:
            session.add(Comment(answer_id, user_id, text))
            session.commit()
            
    @staticmethod
    def delete(answer_id, user_id):
        for comment in session.query(Comment).filter(
                Comment.answer_id == answer_id, Comment.user_id == user_id):
            session.delete(comment)
            session.commit()
        
    @staticmethod
    def get(answer_id, user_id):
        return session.query(Comment).filter(Comment.answer_id == answer_id,
            Comment.user_id == user_id).all()
