from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base
from datetime import datetime
from base import BaseEntity

class AnswerChoiceModel(Base,BaseEntity):
    __tablename__ = 'answerchoice'

    user_id = Column(String,nullable=False)
    answer_id0 = Column(Integer, ForeignKey('answer.id'),nullable=False)
    answer0 = relationship('Answer', foreign_keys=[answer_id0])
    answer_id1 = Column(Integer,ForeignKey('answer.id'),nullable=False)
    answer1 = relationship('Answer', foreign_keys=[answer_id1])
    choice = Column(Boolean,nullable=False)
    

