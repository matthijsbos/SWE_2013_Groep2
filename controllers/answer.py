from models import answer
from flask import render_template
import datetime

class Answer():
    def __init__(self,request):
        self.request = request

    def render(self):
        #dummy shit, get some real data
        qText = 'wat is het antwoord op deze dummy vraag?'
        uID = -11
        qID = -1        
        timerD = 10
        
        if self.request.form.has_key('answerText'):
            #save answer
            answerText = self.request.form['answerText']
            aID = answer.AnswerModel.getAnswerID(uID, qID)
            
            succes = "false"
            if self.timeLeft(aID, timerD):            
                answer.AnswerModel.updateAnswer(aID, answerText)
                succes = "true"
                
            return render_template('answersaved.html', succes=succes)

        elif self.request.form.has_key('showall'):
            #Render all
            return render_template('showanswers.html',answers=answer.AnswerModel.get_all())
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