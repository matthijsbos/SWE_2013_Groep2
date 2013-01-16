from models import answer
from flask import render_template
import datetime

class Answer():
    def __init__(self,request):
        self.request = request

    def render(self):
        #dummy shit, get some real data
        qText = 'wat is het antwoord op deze dummy vraag?'
        uID = -1
        qID = -1
        timerD = 10

        if self.request.form.has_key('answerText'):
            #save answer
            answerText = self.request.form['answerText']
            aID = answer.AnswerModel.getAnswerID(uID, qID)
            
            currentTime = datetime.datetime.now()
            timeAnswered = answer.AnswerModel.getTimeStamp(aID)
            difference = currentTime - timeAnswered
            seconds = difference.days * 86400 + difference.seconds
            
            succes = "false"
            if seconds < timerD:            
                answer.AnswerModel.updateAnswer(aID, answerText)
                succes = "true"
                
            return render_template('answersaved.html', succes=succes)

        elif self.request.form.has_key('showall'):
            #Render all
            return render_template('showanswers.html',answers=answer.AnswerModel.get_all())
        else:            
            if answer.AnswerModel.alreadyAnswered(uID, qID):
                answer.AnswerModel.save(qID,uID,"")
                aID = answer.AnswerModel.getAnswerID(uID, qID)
                return render_template('answer.html',questionID=qID,userID=uID,questionText=qText,timerDuration=timerD, go="true", answerID=aID)
            else:
                return render_template('answer.html',questionID=qID,userID=uID,questionText=qText,timerDuration=timerD, go="false")