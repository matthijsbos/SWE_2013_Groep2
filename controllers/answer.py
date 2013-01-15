from models import answer
from flask import render_template

class Answer():
    def __init__(self,request):
        self.request = request

    def render(self):
        #dummy shit, get some real data
        qText = 'wat is het antwoord op deze dummy vraag?'
        uID = -1
        qID = -1

        if self.request.form.has_key('answerText'):
            #save answer
            questionID = self.request.form['questionID']
            userID = self.request.form['userID']
            answerText = self.request.form['answerText']

            answer.AnswerModel.save(questionID,userID,answerText)
            return render_template('answersaved.html')
        elif self.request.form.has_key('showall'):
            #Render all
            return render_template('showanswers.html',answers=answer.AnswerModel.getall())
        else:
            return render_template('answer.html',questionID=qID,userID=uID,questionText=qText)
