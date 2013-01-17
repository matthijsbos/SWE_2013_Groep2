from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base
from datetime import datetime
from base import BaseEntity

class AnswerChoiceModel(Base,BaseEntity):
    __tablename__ = 'answerchoice'

    user_id = Column(String,nullable=False)
    best_answer_id = Column(Integer,ForeignKey('answer.id'), nullable=False)
    #best_answer = relationship('AnswerModel', foreign_keys=[best_answer_id])
    other_answer_id = Column(Integer, ForeignKey('answer.id'), nullable=False)
    #other_answer = relationship('AnswerModel', foreign_keys=[other_answer_id])

    def __init__(self, user_id, best_answer_id, other_answer_id):
        self.user_id = user_id
        self.best_answer_id = best_answer_id
        self.other_answer_id = other_answer_id

