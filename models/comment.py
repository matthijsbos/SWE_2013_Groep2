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
    user_id = Column(Integer)
    text = Column(String)
    
    def __init__(self, answer_id, user_id, text):
        self.answer_id = answer_id
        self.user_id = user_id
        self.text = text
        
    def __repr__(self):
        return "<Comment(aid='%d', uid='%d', '%s')" % (self.answer_id,
            self.user_id, self.text)
    
    @staticmethod        
    def add(answer_id, user_id, text):
        session.add(Comment(answer_id, user_id, text))
        session.commit()
    
    @staticmethod
    def edit(comment_id, answer_id, user_id, text):
        session.query(Comment).filter(Comment.id == comment_id,
                Comment.answer_id == answer_id, 
                Comment.user_id == user_id).update(Comment.text = text)
        session.commit()
                
    # user_id is not necessary since comment id is unique. However, this allows
    # for easy security check by passing the user id from session data.
    @staticmethod
    def delete(comment_id, user_id):
        for comment in session.query(Comment).filter(Comment.id == comment_id,
                Comment.user_id == user_id):
            session.delete(comment)
            session.commit()
            
    @staticmethod
    def delete(answer_id, user_id):
        for comment in session.query(Comment).filter(
                Comment.answer_id == answer_id, Comment.user_id == user_id):
            session.delete(comment)
        session.commit()