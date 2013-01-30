from dbconnection import engine, Base, session
from sqlalchemy import String,Column,Float,Integer
from basemodel import BaseEntity
from user import UserModel

class UserHistoryModel(Base, BaseEntity):
    __tablename__ = 'user_history'
    __table_args__ = {'sqlite_autoincrement': False}

    userid = Column(String)    #
    trust = Column(Float)      # trust rating at this time
    answered = Column(Integer) # amount of questions answered at this time
    asked = Column(Integer)    # amount of eligible questions at this time
    
    def __init__(self, a, b, c, d):
        self.userid   = a
        self.trust    = b
        self.answered = c
        self.asked    = d
        
    @staticmethod
    def get_by_user_id(uid):
        return session.query(UserHistoryModel).filter(UserHistoryModel.userid == uid).order_by(UserHistoryModel.created.asc())
        
    @staticmethod
    def get_user_latest_data(uid):
        return session.query(UserHistoryModel).filter(UserHistoryModel.userid == uid)[:1]
        
    @staticmethod
    def set_trust(uid, trust):
        thing = UserHistoryModel.get_user_latest_data(uid)
        thing.trust = trust        
        session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
        session.commit
        
    @staticmethod
    def inc_answered(uid):
        thing = UserHistoryModel.get_user_latest_data(uid)
        thing.answered = thing.answered + 1      
        session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
        session.commit
        
    @staticmethod
    def inc_asked(uid):
        thing = UserHistoryModel.get_user_latest_data(uid)
        thing.asked = thing.asked + 1      
        session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
        session.commit

Base.metadata.create_all(engine)
