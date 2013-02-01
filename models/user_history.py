from dbconnection import engine, Base, session
from sqlalchemy import String,Column,Float,Integer,Boolean
from basemodel import BaseEntity

class UserHistoryModel(Base, BaseEntity):
    __tablename__ = 'user_history'
    __table_args__ = {'sqlite_autoincrement': False}

    userid = Column(String)     #
    source_id = Column(Integer) # question id of adjusting, or 0 if another source had influence
    trust = Column(Float)       # trust rating at this time
    answered = Column(Integer)  # amount of questions answered at this time
    asked = Column(Integer)     # amount of eligible questions at this time
    qanswered = Column(Boolean) #

    def __init__(self, a, b, c, d):
        self.userid    = a
        self.trust     = b
        self.answered  = c
        self.asked     = d

    @staticmethod
    def get_by_user_id(uid):
        return session.query(UserHistoryModel).filter(UserHistoryModel.userid == uid).order_by(UserHistoryModel.created.asc())[:1]
        
    @staticmethod
    def get_by_user_id_more(uid):
        return session.query(UserHistoryModel).filter(UserHistoryModel.userid == uid).order_by(UserHistoryModel.created.asc())

    @staticmethod
    def get_user_latest_data(uid):
        return session.query(UserHistoryModel).filter(UserHistoryModel.userid == uid).order_by(UserHistoryModel.created.desc()).first()
        
    @staticmethod
    def get_by_user_and_q_id(uid, qid):
        return session.query(UserHistoryModel).filter(UserHistoryModel.userid == uid, UserHistoryModel.source_id == qid)


Base.metadata.create_all(engine)
