# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 12:47:32 2013

@author: Mustafa Karaalioglu
"""
from sqlalchemy import Column, Integer, String, ForeignKey

from dbconnection import engine, session, Base
from baseentity import BaseEntity

class Schedule(Base, BaseEntity):
    __tablename__ = "Schedule"
    
    answer_id = Column(Integer, ForeignKey('answer.id', ondelete='CASCADE'))    
    user_id = Column(String)
    
    def __init__(self, answer_id, user_id):
        self.answer_id = answer_id
        self.user_id = user_id
        
    @staticmethod
    def get_answer(user_id):
        return session.query(Schedule).filter(
            Schedule.user_id == user_id).first()
            
    @staticmethod
    def add(answer_id, user_id):
        if session.query(Schedule).filter(Schedule.answer_id == answer_id,
                Schedule.user_id == user_id).first() is not None:
            session.add(Schedule(answer_id, user_id))
            session.commit()
    
    # tuple list of (answer_id, user_id)
    @staticmethod
    def add_list(list):
        for a_id, u_id in list:
            if session.query(Schedule).filter(Schedule.answer_id == a_id,
                    Schedule.user_id == u_id).first() is not None:
                session.add(Schedule(a_id, u_id))
        
        session.commit()
            
    @staticmethod
    def delete(answer_id, user_id):
        for schedule in session.query(Schedule).filter(
                Schedule.answer_id == answer_id, Schedule.user_id == user_id):
            session.delete(schedule)
            session.commit()
            

Base.metadata.create_all(engine)