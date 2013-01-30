from dbconnection import engine, Base, session
from sqlalchemy import String,Column,Float,Integer
from basemodel import BaseEntity

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
        
    # method creates a new history entry by copying the last known history
    # entry of the student, and updating the 'trust' column
    @staticmethod
    def set_trust(uid, trust):
        thing = UserHistoryModel.get_user_latest_data(uid)
        thing.trust = trust        
        session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
        session.commit
        
    # method creates a new history entry by copying the last known history
    # entry of the student, and updating the 'answered' column
    @staticmethod
    def inc_answered(uid):
        thing = UserHistoryModel.get_user_latest_data(uid)
        thing.answered = thing.answered + 1
        # make sure answered cannot exceed asked, which would result in
        # participation data higher than 100%
        if (thing.answered > thing.asked):
            thing.asked = thing.answered
        session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
        session.commit
        
    # method creates a new history entry by copying the last known history
    # entry of the student, and updating the 'asked' column
    @staticmethod
    def inc_asked(uid):
        thing = UserHistoryModel.get_user_latest_data(uid)
        thing.asked = thing.asked + 1      
        session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
        session.commit

Base.metadata.create_all(engine)
