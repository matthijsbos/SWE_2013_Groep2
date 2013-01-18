from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base
from datetime import datetime
from basemodel import BaseEntity

K = 100
class AnswerChoiceModel(Base,BaseEntity):
    __tablename__ = 'answerchoice'

    user_id = Column(String,nullable=False)
    best_answer_id  = Column(Integer, ForeignKey('answer.id'), nullable=False)
    best_answer = relationship('AnswerModel', primaryjoin='AnswerChoiceModel.best_answer_id == AnswerModel.id')
    other_answer_id = Column(Integer, ForeignKey('answer.id'), nullable=False)
    other_answer = relationship('AnswerModel', primaryjoin='AnswerChoiceModel.other_answer_id == AnswerModel.id')
    #other_answer = relationship('AnswerModel', foreign_keys=other_answer_id)

    def __init__(self, user_id, best_answer_id, other_answer_id):
        self.user_id = user_id
        self.best_answer_id = best_answer_id
        self.other_answer_id = other_answer_id

    def winningProbability(rating1, rating2) :
        return 1.0 / (1.0 + (10.0**((rating2 - rating1) / 400.0)))

    def newRating(winner, loser) :
        expectedScore = winningProbability(winner, loser)
        winnerRating = winner + K * (1 - winningProbability(winner, loser))
        loserRating = loser + K * (0 - winningProbability(loser, winner))
        return winnerRating, loserRating
