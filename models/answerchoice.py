from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base
from datetime import datetime
from basemodel import BaseEntity
from models.answer import AnswerModel
from models.user import UserModel
from models.user_history import UserHistoryMode

class AnswerChoiceModel(Base,BaseEntity):

    __tablename__ = 'answerchoice'

    #inherited from BaseEntity
    #id
    #created
    #modified
    user_id = Column(String,nullable=False)
    best_answer_id  = Column(Integer, ForeignKey('answer.id'), nullable=False)
    best_answer = relationship('AnswerModel', primaryjoin='AnswerChoiceModel.best_answer_id == AnswerModel.id')
    other_answer_id = Column(Integer, ForeignKey('answer.id'), nullable=False)
    other_answer = relationship('AnswerModel', primaryjoin='AnswerChoiceModel.other_answer_id == AnswerModel.id')

    def __init__(self, user_id, best_answer_id, other_answer_id):
        self.user_id = user_id
        self.best_answer_id = best_answer_id
        self.other_answer_id = other_answer_id
        self.calcNewRating()
        self.calcNewTrust()

    def calcNewRating(self):
        K = UserModel.getTrust(self.user_id) / 20.0
        newRating = AnswerModel.newRating(self.best_answer_id, self.other_answer_id, K)
        AnswerModel.setRanking(self.best_answer_id, newRating[0])
        AnswerModel.setRanking(self.other_answer_id, newRating[1])

    def calcNewTrust(self) :
        winId = AnswerModel.getUserIdByAnswerId(self.best_answer_id)
        losId = AnswerModel.getUserIdByAnswerId(self.other_answer_id)
        newTrust = UserModel.newTrust(winId, losId)
        UserHistoryModel(winId, newTrust[0])
        UserHistoryModel(losId, newTrust[1])
