from dbconnection import engine, Base, session
from sqlalchemy import String,Column,Float,Integer,Boolean
from basemodel import BaseEntity
from user import UserModel
from answer import AnswerModel

class UserHistoryModel(Base, BaseEntity):
    __tablename__ = 'user_history'
    __table_args__ = {'sqlite_autoincrement': False}

    userid = Column(String)     #
    source_id = Column(Integer) # question id of adjusting, or 0 if another source had influence
    trust = Column(Float)       # trust rating at this time
    answered = Column(Integer)  # amount of questions answered at this time
    asked = Column(Integer)     # amount of eligible questions at this time
    qanswered = Column(Bool)    #

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
        return session.query(UserHistoryModel).filter(UserHistoryModel.userid == uid).order_by(UserHistoryModel.created.asc()).first()

    # method creates a new history entry by copying the last known history
    # entry of the student, and updating the 'trust' column
    # also copies over the trust value to the current one in UserModel
    @staticmethod
    def set_trust(uid, trust):
        thing = UserHistoryModel.get_user_latest_data(uid)
        thing.trust = trust
        session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
        session.commit
        # also update current trust, in UserModel
        UserModel.setTrust(uid, trust)

    @staticmethod
    def update_question_stats(cls, qid):
        temp = UserModel.get_all(cls)
        for element in temp:
            UserHistoryModel.inc_question_stats(element.userid, qid)

    # method that adds a new history entry by copying the last known history
    # entry for this student, and updating 'trust' column
    @staticmethod
    def inc_question_stats(uid, qid):
        answered = (session.query(AnswerModel).filter_by(userID=uid, questionID=qid))
        recorded = (session.query(UserHistoryModel).filter_by(userid=uid, source_id=qid))
        if recorded:
            boole = recorded.qanswered

        thing = UserHistoryModel.get_user_latest_data(uid)

        # in case the question was immediately answered
        if (answered != None) and (recorded == None):
            thing = UserHistoryModel.get_user_latest_data(uid)
            thing.asked = thing.asked + 1
            thing.answered = thing.answered + 1
            thing.qanswered = True
            session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
            session.commit

        # in case the question was not answered at all
        elif (answered == None) and (recorded == None):
            thing = UserHistoryModel.get_user_latest_data(uid)
            thing.asked = thing.asked + 1
            #thing.answered = thing.answered + 0
            thing.qanswered = False
            session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
            session.commit

        # in case the question was previously asked, but only answered after unlocking it
        elif (answered != None) and (recorded != None) and not (boole):
            thing = UserHistoryModel.get_user_latest_data(uid)
            #thing.asked = thing.asked + 0
            thing.answered = thing.answered + 1
            thing.qanswered = True
            session.add(UserHistoryModel(thing.userid, thing.trust, thing.answered, thing.asked))
            session.commit

Base.metadata.create_all(engine)
