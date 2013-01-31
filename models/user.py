from dbconnection import engine, session, Base, exc
from sqlalchemy import String,Column


class UserModel(Base):
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': False}

    userid = Column(String, primary_key=True)
    username = Column(String)

    @classmethod
    def get_all(cls):
        return session.query(cls).filter().all()

    @classmethod
    def by_user_id(cls,uid):
        return session.query(cls).filter(cls.userid == uid).first()

    @staticmethod
    def save(uid,uname):
        user = UserModel.by_user_id(uid)
        if user is None:
            session.add(UserModel(userid=uid,username=uname))
            session.commit()
        elif user.username != uname:
            user.username = uname
            session.commit()

Base.metadata.create_all(engine)
