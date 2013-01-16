from models import answer, question
from flask import render_template,g
import datetime
import sqlalchemy.orm.exc as sqlalchemyExp

class Answer():
    def __init__(self,request):
        self.request = request

    def render(self):
        #dummy shit, get some real data
        qText = 'wat is het antwoord op deze dummy vraag?'
        uID = 23455#g.lti.get_user_id()
        qID = -1        
        timerD = 10
        
        #Post should be real data
        if self.request.method == 'POST' and self.request.form.has_key('questionID'):
            try:
                qID = int(self.request.form['questionID'])
                qText = question.Question.by_id(qID).question
            except(sqlalchemyExp.NoResultFound):
                pass
            except Exception as e:
                return e
        
        if self.request.form.has_key('answerText'):
            #save answer
            answerText = self.request.form['answerText']
            aID = answer.AnswerModel.getAnswerID(uID, qID)
            
            succes = "false"
            if self.timeLeft(aID, timerD, 0):            
                answer.AnswerModel.updateAnswer(aID, answerText)
                succes = "true"
                
            return render_template('answersaved.html', succes=succes)

        elif self.request.form.has_key('showall'):
            #Render all
            return self.render_all()
        elif self.request.form.has_key('viewanswer'):
            #show answer
            aid = int(self.request.form['id'])
            return render_template('editanswer.html', answer=answer.AnswerModel.by_id(aid))
        elif self.request.form.has_key('reviewAnswer'):
            #save review answer
            questionID = int(self.request.form['questionID'])
            userID = self.request.form['userID']
            reviewAnswer = self.request.form['reviewAnswer']
            edit = int(self.request.form['edit'])
            answer.AnswerModel.savereview(questionID,userID,reviewAnswer,edit)
            return render_template('answersaved.html')
        elif self.request.form.has_key('removeAnswer'):
            id = int(self.request.form['id'])
            answer.AnswerModel.remove_by_id(id)
            return render_template('answersaved.html')
        else:
            if answer.AnswerModel.checkAnswerExist(uID, qID):
                aID = answer.AnswerModel.getAnswerID(uID, qID)
                if self.timeLeft(aID, timerD, 0):                                       
                    return render_template('answer.html',questionID=qID,userID=uID,questionText=qText,timerDuration=self.timeLeft(aID, timerD, 1), go="true", answerID=aID)
                else:
                    return render_template('answer.html',questionID=qID,userID=uID,questionText=qText,timerDuration=timerD, go="false")
            else:
                answer.AnswerModel.save(qID,uID,"")                
                return render_template('answer.html',questionID=qID,userID=uID,questionText=qText,timerDuration=timerD, go="true")
    
    def timeLeft(self, aID, timerD, giveTime):
        currentTime = datetime.datetime.now()
        timeAnswered = answer.AnswerModel.getTimeStamp(aID)
        difference = currentTime - timeAnswered
        seconds = difference.days * 86400 + difference.seconds
        
        if giveTime == 1:
            minutes = int((timerD - seconds) / 60)
            seconds = (timerD - seconds)%60
            return ""+str(minutes)+":"+str(seconds)
                    
        if seconds < timerD:
            return True
        else:
            return False        
       
    def render_filtered(self):
        postdata = self.request.form

        args = {}
        if self.request.method == "POST":
            if postdata.has_key("questionID") and len(postdata["questionID"]) > 0:
                args["questionID"] = postdata["questionID"]
            if postdata.has_key("userID") and len(postdata["userID"]) > 0:
                args["userID"] = postdata["userID"]
            if postdata.has_key("id") and len(postdata["id"]) > 0:
                args["id"] = postdata["id"]

        return render_template('answerfilter.html',answers=answer.AnswerModel.get_filtered(**args))

    def render_all(self):
        #Render all
        return render_template('showanswers.html',answers=answer.AnswerModel.get_all())
