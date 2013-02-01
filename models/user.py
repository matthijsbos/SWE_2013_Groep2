from dbconnection import engine, session, Base, exc
from sqlalchemy import String,Column,Float
from basemodel import BaseEntity
from question import Question
from user_history import UserHistoryModel

class UserModel(Base):
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': False}

    userid = Column(String, primary_key=True)
    username = Column(String)
    trust = Column(Float)
    
    @classmethod
    def get_all(cls):
        return session.query(cls).filter().all()

    @classmethod
    def by_user_id(cls,uid):
        return session.query(cls).filter(cls.userid == uid).first()

    @staticmethod
    def get_by_username(uid):
        return session.query(UserModel).filter(UserModel.username == uid)

    @staticmethod
    def save(uid,uname):
        user = UserModel.by_user_id(uid)
        if user is None:
            # add user to UserModel
            tmp = UserModel(userid=uid,username=uname)
            tmp.trust = 1000.0
            session.add(tmp)
            session.commit()
            # add user's first entry to UserHistoryModel
            history = UserHistoryModel(uid, 1000.0, 0, 0)
            session.add(history)
            session.commit()
        elif user.username != uname:
            user.username = uname
            session.commit()

    @staticmethod
    def getTrust(uID):
        user = session.query(UserModel).filter_by(userid=uID).one()
        return user.trust

    @staticmethod
    def setTrust(uID, trust):
        # set current trust (in usermodel)
        user = session.query(UserModel).filter_by(userid=uID).one()
        user.trust = trust
        # fetch last known history record
        old = UserHistoryModel.get_user_latest_data(uID)
        print old.answered
        print old.asked
        # create a new trust entry in userhistory
        history = UserHistoryModel(uID, trust, old.answered, old.asked)
        session.add(history)
        session.commit()

    @staticmethod
    def winningProbability(rating1, rating2) :
        return 1.0 / (1.0 + (10.0**((rating2 - rating1) / 400.0)))

    @staticmethod
    def newTrust(winnerId, loserId) :
        K = 100.0
        winnerTrust = UserModel.getTrust(winnerId)
        loserTrust = UserModel.getTrust(loserId)
        newWinnerTrust = winnerTrust + (K * (1.0 - UserModel.winningProbability(winnerTrust, loserTrust)))
        newLoserTrust = loserTrust + (K * (0.0 - UserModel.winningProbability(loserTrust, winnerTrust)))
        return newWinnerTrust, newLoserTrust

Base.metadata.create_all(engine)
