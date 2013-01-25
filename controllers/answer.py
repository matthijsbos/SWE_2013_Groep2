from models import answer, question
from models.question import Question
from models.answer import AnswerModel
from flask import render_template, g, request, redirect
import datetime
import time
import sqlalchemy.orm.exc as sqlalchemyExp


class Answer():
    def __init__(self, request):
        self.request = request

    def render(self):
        try:
            qID = int(self.request.values['questionID'])
            uID = g.lti.get_user_id()
        except:
            return abort(404)

        q = question.Question.by_id(qID)
        if q is not None:
            qText = q.question
            questionStartTime = q.modified;
            timerD = q.time

        if 'answerText' in self.request.values:
            return self.saveAnswer(uID, qID, timerD, questionStartTime)
        elif 'showall' in self.request.values:
            # Render all
            return self.render_all()
        elif 'viewanswer' in self.request.values:
            # show answer
            return self.viewAnswer()
        elif 'reviewAnswer' in self.request.values:
            # save review answer
            return self.saveReviewAnswer()
        elif 'removeAnswer' in self.request.values:
            return self.removeAnswer()
        else:
            return self.answerQuestion(uID, qID, qText, timerD, questionStartTime)

    @staticmethod
    def renderanswerform():
        try:
            questionid = int(request.values['question_id'])
            question = Question.by_id(questionid)
        except:
            return abort(404)
        return render_template('student_answer.html', question = question)

    @staticmethod
    def save():
        try:
            questionid = int(request.values['questionid'])
            question = Question.by_id(questionid)
            text = request.values['text']
            userid = g.lti.get_user_id()
        except:
            return abort(404)

        if AnswerModel.question_valid(questionid):
            AnswerModel.save(questionid, userid, text)

        return redirect('/index_student')
        
    def saveAnswer(self, uID, qID, timerD, questionStartTime):
        # save answer
        answerText = self.request.form['answerText']

        flag = "false"
        if self.timeLeft(timerD, 0, questionStartTime):
            if answer.AnswerModel.checkAnswerExist(uID, qID):
                aID = answer.AnswerModel.getAnswerID(uID, qID)
                answer.AnswerModel.updateAnswer(aID, answerText)
            else:
                answer.AnswerModel.save(qID, uID, answerText)
            flag = "true"

        return redirect('/index_student')

    def viewAnswer(self):
        aid = int(self.request.form['id'])
        return render_template('editanswer.html', answer=answer.AnswerModel.by_id(aid))

    def saveReviewAnswer(self):
        questionID = int(self.request.form['questionID'])
        userID = self.request.form['userID']
        reviewAnswer = self.request.form['reviewAnswer']
        edit = int(self.request.form['edit'])
        answer.AnswerModel.savereview(
            questionID, userID, reviewAnswer, edit)
        return redirect('/index_student')

    def removeAnswer(self):
        id = int(self.request.form['id'])
        answer.AnswerModel.remove_by_id(id)
        return redirect('/index_student')
        #return render_template('answersaved.html', flag='removed')

    def answerQuestion(self, uID, qID, qText, timerD, questionStartTime):
        if answer.AnswerModel.checkAnswerExist(uID, qID):
            aID = answer.AnswerModel.getAnswerID(uID, qID)
            if self.timeLeft(timerD, 0, questionStartTime):
                return redirect('/index_student')
                #return render_template('answer.html', questionID=qID, userID=uID, questionText=qText, timerDuration=timerD, date=time.mktime(questionStartTime.timetuple()), go="true")
            else:
                return redirect('/index_student')
                #return render_template('answer.html', questionID=qID, userID=uID, questionText=qText, timerDuration=timerD, date=time.mktime(questionStartTime.timetuple()), go="false")
        else:
            #answer.AnswerModel.save(qID, uID, "")
            return redirect('/index_student')
            #return render_template('answer.html', questionID=qID, userID=uID, questionText=qText, timerDuration=timerD, date=time.mktime(questionStartTime.timetuple()), go="true")

    def timeLeft(self, timerD, giveTime, questionStartTime):
        currentTime = datetime.datetime.now()
        timeAnswered = questionStartTime
        difference = currentTime - timeAnswered
        seconds = difference.days * 86400 + difference.seconds

        if giveTime == 1:
            return timerD - seconds

        if seconds < timerD + 2:
            return True
        else:
            return False

    def render_filtered(self):
        postdata = self.request.form

        args = {}
        if self.request.method == "POST":
            if "questionID" in postdata and len(postdata["questionID"]) > 0:
                args["questionID"] = postdata["questionID"]
            if "userID" in postdata and len(postdata["userID"]) > 0:
                args["userID"] = postdata["userID"]
            if "id" in postdata and len(postdata["id"]) > 0:
                args["id"] = postdata["id"]

        return render_template('answerfilter.html', answers=answer.AnswerModel.get_filtered(**args))

    def render_results(self):
        args = {"questionID": request.values["questionid"]}
        return render_template('rankresults.html', answers=answer.AnswerModel.get_filtered(**args))
        
    def render_all(self):
        # Render all
        return render_template('showanswers.html', answers=answer.AnswerModel.get_all())

    def render_filtered_by_questionid(self,questionid):
        postdata = self.request.form
        args = {"questionID": questionid}

        if self.request.method == "POST":
            if "userID" in postdata and len(postdata["userID"]) > 0:
                args["userID"] = postdata["userID"]
            if "id" in postdata and len(postdata["id"]) > 0:
                args["id"] = postdata["id"]

        return render_template('answerfilter_by_questionid.html', answers=answer.AnswerModel.get_filtered(**args))

    def studenthistory(self):
        return render_template('studenthistory.html')
        
    def studenthistory_result(self):
        return render_template('studenthistory_result.html', studid=answer.AnswerModel.get_answers_by_userid(request.values['sid']))
