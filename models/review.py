# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:00:23 2013

@author: Robin van Rijn
"""

from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from dbconnection import engine, session, Base
from models.answer import AnswerModel
from basemodel import BaseEntity
from models.user import UserModel


class Review(Base, BaseEntity):
    __tablename__ = 'Review'
    answer_id = Column(Integer, ForeignKey('answer.id', ondelete='CASCADE'))
    user_id = Column(String)
    text = Column(String)
    rating = Column(Integer)

    def __init__(self, answer_id, user_id, rating, text):
        self.answer_id = answer_id
        self.user_id = user_id
        self.rating = rating
        self.text = text

    def __repr__(self):
        return "<Review(aid='%d', uid='%s', '%s')" % (self.answer_id,
            self.user_id, self.text)

    @staticmethod
    def add(answer_id, user_id, rating, text):
        if session.query(Review).filter(Review.answer_id == answer_id,
               Review.user_id == user_id).first() is not None:
        session.add(Review(answer_id, user_id, rating, text))
            session.commit()

    @staticmethod
    def delete(answer_id, user_id):
        for review in session.query(Review).filter(
                Review.answer_id == answer_id, Review.user_id == user_id):
            session.delete(review)
            session.commit()

    @staticmethod
    def get(answer_id, user_id):
        return session.query(Review).filter(Review.answer_id == answer_id,
            Review.user_id == user_id).all()

    def updateTrust(self):
        trust = UserModel.getTrust(user_id) + ((self.rating * 25.0) - 75.0)
        UserModel.setTrust(self.user_id, trust)            

    @staticmethod
    def get_list(answer_id):
        return session.query(Review).filter(Review.answer_id==answer_id).all()
