from models import answer
from flask import render_template

class Answer():
    def __init__(self,request):
        self.request = request

    def render(self):
        #dummy shit, get some real data
        qText = 'wat is het antwoord op deze dummy vraag?'
        uID = 1
        qID = -1

        if self.request.form.has_key('answerText'):
            #save answer
            questionID = int(self.request.form['questionID'])
            userID = int(self.request.form['userID'])
            answerText = self.request.form['answerText']
            answer.AnswerModel.save(questionID,userID,answerText)
            return render_template('answersaved.html')
        elif self.request.form.has_key('showall'):
            #Render all
            return render_template('showanswers.html',answers=answer.AnswerModel.get_all())
        elif self.request.form.has_key('viewanswer'):
            #show answer
            aid = int(self.request.form['id'])
            return render_template('editanswer.html', answer=answer.AnswerModel.by_id(aid))
        elif self.request.form.has_key('reviewAnswer'):
            #save review answer
            questionID = int(self.request.form['questionID'])
            userID = int(self.request.form['userID'])
            reviewAnswer = self.request.form['reviewAnswer']
            weight = int(self.request.form['weight'])
            answer.AnswerModel.savereview(questionID,userID,reviewAnswer,weight)
            return render_template('answersaved.html')
        else:
            return render_template('answer.html',questionID=qID,userID=uID,questionText=qText)
