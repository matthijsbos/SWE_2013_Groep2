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
            id = int(self.request.form['id'])
            return render_template('editanswer.html', answer=answer.AnswerModel.by_id(id))
        elif self.request.form.has_key('reviewAnswer'):
            #save review answer
            questionID = int(self.request.form['questionID'])
            userID = int(self.request.form['userID'])
            reviewAnswer = self.request.form['reviewAnswer']
            edit = int(self.request.form['edit'])
            answer.AnswerModel.savereview(questionID,userID,reviewAnswer,edit)
            return render_template('answersaved.html')
        elif self.request.form.has_key('removeAnswer'):
            id = int(self.request.form['id'])
            answer.AnswerModel.remove_by_id(id)
            return render_template('answersaved.html')
        else:
            return render_template('answer.html',questionID=qID,userID=uID,questionText=qText)
