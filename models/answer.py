from datetime import datetime, timedelta
from sqlalchemy import *
from sqlalchemy.orm import relationship
from dbconnection import engine, session, Base, exc
from basemodel import BaseEntity
from question import Question
from user import UserModel
from user_history import UserHistoryModel

class AnswerModel(Base, BaseEntity):
    __tablename__ = 'answer'

    text = Column(String)
    questionID = Column(Integer)
    userID = Column(String)
    edit = Column(Integer)
    ranking = Column(Float)    
    tags = Column(String)

    def __init__(self,text,questionID,userID,edit,ranking, tags=''):
        self.text = text
        self.questionID = questionID
        self.userID = userID
        self.edit = edit
        self.ranking = ranking
        self.tags = tags

    @property
    def username(self):
        user = UserModel.by_user_id(self.userID)
        if user is None:
            return self.userID
        return user.username

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

    @staticmethod
    def get_question_answers(question_id):
        return session.query(AnswerModel).filter(
			AnswerModel.questionID==question_id)

    @staticmethod
    def get_answers_ordered_by_rank(question_id):
        return session.query(AnswerModel).filter(AnswerModel.questionID==question_id).order_by(AnswerModel.ranking.desc())
        #return session.query(AnswerModel).filter(AnswerModel.questionID==question_id).order_by(AnswerModel.ranking.desc())

    @staticmethod
    def update_answer(answerID, answerText):
        session.query(AnswerModel).filter_by(id=answerID).update(
            {"text": answerText}, synchronize_session=False)

    @staticmethod
    def save(questionID, userID, answerText):
        try:
            ranking = ((session.query(UserModel).filter_by(userid=userID).one().trust - 1000.0) / 4) + 1000.0
        except exc.InvalidRequestError:
            ranking = 1000.0
        session.add(AnswerModel(questionID=questionID, userID=userID, text=answerText, edit=0, ranking=ranking))
        session.commit()
        # add to history -> TODO
        # should be replaced to trip when a question closes
        # AnswerModel.update_q_history(questionID)

    @staticmethod
    def update_q_history(qid):
        temp = UserModel.get_all()
        for element in temp:
            AnswerModel.add_q_stats(element.userid, qid)

    @staticmethod
    def add_q_stats(uid, qid):
        answered = (session.query(AnswerModel).filter_by(userID=uid, questionID=qid)).one()
        recorded = (session.query(UserHistoryModel).filter_by(userid=uid, source_id=qid)).first()
        if (recorded != None):
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

    @staticmethod
    def get_answer_id(uID, qID):
        answer = session.query(AnswerModel).filter_by(questionID=qID, userID=uID, edit=0).one()
        return answer.id

    @staticmethod
    def check_answer_exists(uID, qID):
        if engine.dialect.has_table(engine.connect(), "answer"):
            try:
                answer = session.query(AnswerModel).filter_by(questionID=qID, userID=uID, edit=0).one()
                return 1
            except exc.InvalidRequestError:
                return 0
        else:
            return 0

    @staticmethod
    def get_active_questions(userid, courseid):
        anssub = session.query(AnswerModel).filter(AnswerModel.userID == userid).\
            subquery()

        # HACK: I can't figure out how to do timedelta stuff inside a filter,
        #       so that is done after pulling all data... Slow!

        # Need to use the old Alias.c.[columname] when using subquery!
        tmp = session.query(Question).\
                outerjoin(anssub, anssub.c.questionID == Question.id).\
                filter(Question._answerable == True).\
                filter(Question.course_id == courseid)

        #print tmp
        #print [(x.modified + timedelta(seconds=x.time), datetime.now()) for x in tmp]

        questions = []

        for x in tmp:
            if x.time == 0:
                questions.append(x)
            elif x.activate_time + timedelta(seconds=x.time) > datetime.now():
                questions.append(x)

        return questions

    @staticmethod
    def get_answered_active_questions(userid, courseid):
        """
        Exactly the same as get_unanswered_questions except we want the answered
        ones
        """
        anssub = session.query(AnswerModel).filter(AnswerModel.userID == userid).\
            subquery()


        # Need to use the old Alias.c.[columname] when using subquery!
        tmp = session.query(Question).\
                outerjoin(annsub, anssub.c.questionID == Question.id).\
                filter(Question.available == True).\
                filter(Question.course_id == courseid).\
                filter(anssub.c.id != None).all()

        print tmp
        print [(x.modified + timedelta(seconds=x.time), datetime.now()) for x in tmp]

        return [x for x in tmp if x.modified + timedelta(seconds=x.time) >
                datetime.now()]

    @staticmethod
    def question_valid(questionid):
        questionTmp = Question.by_id(questionid)

        return [questionTmp.modified + timedelta(seconds=questionTmp.time) >
                datetime.now()]


    @staticmethod
    def getTimeStamp(answerID):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        return answer.created

    @staticmethod
    def get_ranking(answerID):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        return answer.ranking

    @staticmethod
    def set_ranking(answerID, ranking):
        answer = session.query(AnswerModel).filter_by(id=answerID).one()
        answer.ranking = ranking

    @staticmethod
    def winning_probability(rating1, rating2):
        return 1.0 / (1.0 + (10.0**((rating2 - rating1) / 400.0)))

    @staticmethod
    def get_by_answer_id(answerId) :
        temp = session.query(AnswerModel).filter_by(id=answerId).one()
        return temp

    @staticmethod
    def new_rating(winner, loser, K) :
        winnerRanking = AnswerModel.get_ranking(winner)
        loserRanking = AnswerModel.get_ranking(loser)
        newWinnerRanking = winnerRanking + (K * (1.0 - AnswerModel.winning_probability(winnerRanking, loserRanking)))
        newLoserRanking = loserRanking + (K * (0.0 - AnswerModel.winning_probability(loserRanking, winnerRanking)))
        return newWinnerRanking, newLoserRanking

    @staticmethod
    def get_answers_by_userid(uId):
        return session.query(AnswerModel).filter_by(userID=uId).all()
