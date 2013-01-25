from models import answer, question,user
from flask import g
from utilities import render_template
import datetime
import time
import json
import sqlalchemy.orm.exc as sqlalchemyExp


class Answer():
    def __init__(self, request):
        self.request = request

    def render(self):
        # dummy shit, get some real data
        qText = 'wat is het antwoord op deze dummy vraag?'
        questionStartTime = datetime.datetime.now();
        uID = g.lti.get_user_id()
        qID = -1
        timerD = 25

        # Post should be real data
        if self.request.method == 'POST' and 'questionID' in self.request.form:
            qID = int(self.request.form['questionID'])
            q = question.Question.by_id(qID)
            if q is not None:
                qText = q.question
                questionStartTime = q.activate_time;
                timerD = q.time
        
        print 'Retrieved question information'
        if 'answerText' in self.request.form:
            print self.saveAnswer(uID, qID, timerD, questionStartTime)
            return json.dumps({"result":True})
        elif 'showall' in self.request.form:
            # Render all
            return self.render_all()
        elif 'viewanswer' in self.request.form:
            # show answer
            return self.viewAnswer()
        elif 'reviewAnswer' in self.request.form:
            # save review answer
            return self.saveReviewAnswer()
        elif 'removeAnswer' in self.request.form:
            return self.removeAnswer()
        else:
            return self.answerQuestion(uID, qID, qText, timerD, questionStartTime)

    def saveAnswer(self, uID, qID, timerD, questionStartTime):
        # save answer
        print "ANSW", uID, qID, timerD
        answerText = self.request.form['answerText']

        flag = "false"
        if self.timeLeft(timerD, questionStartTime):
            if answer.AnswerModel.checkAnswerExist(uID, qID):
                aID = answer.AnswerModel.getAnswerID(uID, qID)
                answer.AnswerModel.updateAnswer(aID, answerText)
            else:
                answer.AnswerModel.save(qID, uID, answerText)
            flag = "true"
        print 'Saved answer'
        user.UserModel.save(uID,g.lti.get_user_name())
        print 'Dexter'
        return True#render_template('answersaved.html', flag=flag)

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
        return render_template('answersaved.html', flag='true')

    def removeAnswer(self):
        id = int(self.request.form['id'])
        answer.AnswerModel.remove_by_id(id)
        return render_template('answersaved.html', flag='removed')

    def answerQuestion(self, uID, qID, qText, timerD, questionStartTime):
        if answer.AnswerModel.checkAnswerExist(uID, qID):
            aID = answer.AnswerModel.getAnswerID(uID, qID)
            if self.timeLeft(timerD, questionStartTime):
                return render_template('answer.html', questionID=qID, userID=uID, questionText=qText, timerDuration=timerD, date=time.mktime(questionStartTime.timetuple()), go="true")
            else:
                return render_template('answer.html', questionID=qID, userID=uID, questionText=qText, timerDuration=timerD, date=time.mktime(questionStartTime.timetuple()), go="false")
        else:
            #answer.AnswerModel.save(qID, uID, "")
            return render_template('answer.html', questionID=qID, userID=uID, questionText=qText, timerDuration=timerD, date=time.mktime(questionStartTime.timetuple()), go="true")

    def timeLeft(self, timerD, questionStartTime):
        currentTime = datetime.datetime.now()
        timeAnswered = questionStartTime
        difference = currentTime - timeAnswered
        seconds = difference.days * 86400 + difference.seconds
        
        if timerD == 0:
            return True
        else:
            if seconds < timerD + 20:
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


