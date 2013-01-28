from dbconnection import engine, session, Base, exc
from sqlalchemy import String,Column,Float


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
        try:
            return session.query(cls).filter(cls.userid == uid).one()
        except:
            return None

    @staticmethod
    def save(uid,uname):
        user = UserModel.by_user_id(uid)
        if user is None:
            session.add(UserModel(userid=uid,username=uname,trust=1000.0))
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
        user = session.query(UserModel).filter_by(userid=uID).one()
        user.trust = trust

Base.metadata.create_all(engine)
