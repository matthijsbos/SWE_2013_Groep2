from sqlalchemy import *
from dbconnection import engine, session, Base, exc
from basemodel import BaseEntity

class AnswerModel(Base, BaseEntity):
    __tablename__ = 'answer'
    __table_args__ = {'sqlite_autoincrement': True}

    text = Column(String)
    questionID = Column(Integer)
    userID = Column(Integer)
    edit = Column(Integer)

    def __repr__(self):
        return self.text + 'Represent'

    def __str__(self):
        return self.text

    @staticmethod
    def savereview(questionID, userID, answerText, edit):
        session.add(AnswerModel(questionID=questionID,
                    userID=userID, text=answerText, edit=edit + 1))
        session.commit()

    def get_question_answers(question_id):
        return session.query(AnswerModel).filter(AnswerModel.questionID==question_id)

    @staticmethod
    def updateAnswer(answerID, answerText):
        session.query(AnswerModel).filter_by(id=answerID).update(
            {"text": answerText}, synchronize_session=False)

    @staticmethod
    def save(questionID, userID, answerText):
        session.add(AnswerModel(
            questionID=questionID, userID=userID, text=answerText, edit=0))
        session.commit()

    @staticmethod
    def getAnswerID(uID, qID):
        answer = session.query(AnswerModel).filter_by(questionID=qID, userID=uID, edit=0).one()
        return answer.id

    @staticmethod
    def checkAnswerExist(uID, qID):
        if engine.dialect.has_table(engine.connect(), "answer"):
            try:
                answer = session.query(AnswerModel).filter_by(questionID=qID, userID=uID, edit=0).one()
                return 1
            except exc.InvalidRequestError:
                return 0
        else:
            return 0

    @staticmethod
    def getTimeStamp(answerID):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        return answer.created


Base.metadata.create_all(engine)
