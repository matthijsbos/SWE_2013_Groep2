from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base
from datetime import datetime
from basemodel import BaseEntity
from models.answer import AnswerModel
from models.user import UserModel
from models.user_history import UserHistoryModel

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
        self.calc_new_rating()
        self.calc_new_trust()

    def calc_new_rating(self):
        K = UserModel.getTrust(self.user_id) / 20.0
        new_rating = AnswerModel.new_rating(self.best_answer_id, self.other_answer_id, K)
        AnswerModel.set_ranking(self.best_answer_id, new_rating[0])
        AnswerModel.set_ranking(self.other_answer_id, new_rating[1])

    """ OBSOLETE - old version
    def calcNewTrust(self) :
        winId = AnswerModel.getUserIdByAnswerId(self.best_answer_id)
        losId = AnswerModel.getUserIdByAnswerId(self.other_answer_id)
        newTrust = UserModel.newTrust(winId, losId)
        UserHistoryModel(winId, newTrust[0], winId.answered, winId.asked)
        UserHistoryModel(losId, newTrust[1], losId.answered, losId.asked)
    """
    def calc_new_trust(self):
        winner    = AnswerModel.get_by_answer_id(self.best_answer_id)
        loser     = AnswerModel.get_by_answer_id(self.other_answer_id)
        winner_h  = UserHistoryModel.get_by_user_id(winner.userID)
        loser_h   = UserHistoryModel.get_by_user_id(loser.userID)
        new_trust = UserModel.newTrust(winner.userID, loser.userID)
        #UserHistoryModel(winner.userID, new_trust[0], winner_h.answered, winner_h.asked)
        #UserHistoryModel(loser.userID, new_trust[1], loser_h.answered, loser_h.asked)
        session.add(UserHistoryModel(winner.userID, new_trust[0], 17, 22))
        session.commit()
        session.add(UserHistoryModel(loser.userID, new_trust[1], 17, 25))
        session.commit()