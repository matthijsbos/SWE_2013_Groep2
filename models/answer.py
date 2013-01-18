from datetime import datetime, timedelta
from sqlalchemy import *
from dbconnection import engine, session, Base, exc
from basemodel import BaseEntity
from question import Question

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
    def get_unanswered_questions(userid,courseid):
        anssub = session.query(AnswerModel).filter(AnswerModel.userID == userid).\
            subquery()

        # HACK: I can't figure out how to do timedelta stuff inside a filter,
        #       so that is done after pulling all data... Slow!

        # Need to use the old Alias.c.[columname] when using subquery!
        tmp = session.query(Question).\
                outerjoin(anssub, anssub.c.questionID == Question.id).\
                filter(Question.available == True).\
                filter(Question.course_id == courseid).\
                filter(anssub.c.id == None).all()

        print tmp
        print [(x.modified + timedelta(seconds=x.time), datetime.now()) for x in tmp]




        return [x for x in tmp if x.modified + timedelta(seconds=x.time) >
                datetime.now()]



    @staticmethod
    def getTimeStamp(answerID):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        return answer.created


Base.metadata.create_all(engine)
