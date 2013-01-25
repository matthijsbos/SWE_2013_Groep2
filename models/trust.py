from sqlalchemy import *
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base, exc
from basemodel import BaseEntity

class TrustModel(Base, BaseEntity):
    __tablename__ = 'trust'

    userID = Column(Integer)
    trust = Column(Float)

    def __init__(self,userID,trust):
        self.userID = userID
        self.trust = trust

    @staticmethod
    def getTrust(uID):
        user = session.query(TrustModel).filter_by(userID=uID).one()
        return user.trust

    @staticmethod
    def setTrust(uID, trust):
        user = session.query(TrustModel).filter_by(userID=uID).one()
        user.trust = trust


