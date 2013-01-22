from datetime import datetime, timedelta
from sqlalchemy import *
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base, exc
from basemodel import BaseEntity
from question import Question

class AnswerModel(Base, BaseEntity):
    __tablename__ = 'answer'

    text = Column(String)
    questionID = Column(Integer,ForeignKey('questions.id'))
    question = relationship('Question')
    userID = Column(Integer)
    edit = Column(Integer)
    ranking = Column(Float)

    def __init__(self,text,questionID,userID,edit,ranking):
        self.text = text
        self.questionID = questionID
        self.userID = userID
        self.edit = edit
        self.ranking = ranking

    def __repr__(self):
        return "<Answer('%s','%s','%s')>" % (self.id,
                                                self.questionID,
                                                self.userID)

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
            questionID=questionID, userID=userID, text=answerText, edit=0, ranking=1000.0))
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
    def get_answered_active_questions(userid, courseid):
        """
        Exactly the same as get_unanswered_questions except we want the answered
        ones
        """
        anssub = session.query(AnswerModel).filter(AnswerModel.userID == userid).\
            subquery()


        tmp = session.query(Question).\
                outerjoin(annsub, anssub.c.questionID == Question.id).\
                filter(Question.available == True).\
                filter(Question.course_id == courseid).\
                filter(anssub.c.id != None).all()

    @staticmethod
    def getTimeStamp(answerID):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        return answer.created

    @staticmethod
    def getRanking(answerID):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        return answer.ranking

    @staticmethod
    def setRanking(answerID, ranking):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        answer.ranking = ranking

    @staticmethod
    def winningProbability(rating1, rating2) :
        return 1.0 / (1.0 + (10.0**((rating2 - rating1) / 400.0)))


    @staticmethod
    def newRating(winner, loser) :
        K = 100
        expectedScore = winningProbability(winner, loser)
        winnerRating = winner + K * (1 - winningProbability(winner, loser))
        loserRating = loser + K * (0 - winningProbability(loser, winner))
        return winnerRating, loserRating
