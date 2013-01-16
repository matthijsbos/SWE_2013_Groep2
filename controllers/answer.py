from models import answer
from flask import render_template

class Answer():
    def __init__(self,request):
        self.request = request

    def render(self):

        if self.request.form.has_key('answerText'):
            #save answer
            questionID = int(self.request.form['questionID'])
            userID = int(self.request.form['userID'])
            answerText = self.request.form['answerText']

            answer.AnswerModel.save(questionID,userID,answerText)
            return render_template('answersaved.html')

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
            userID = int(self.request.form['userID'])
            reviewAnswer = self.request.form['reviewAnswer']
            weight = int(self.request.form['weight'])
            answer.AnswerModel.savereview(questionID,userID,reviewAnswer,weight)
            return render_template('answersaved.html')
        else:
            #dummy shit, get some real data
            qText = 'wat is het antwoord op deze dummy vraag?'
            uID = g.lti.get_user_id()
            qID = -1

            #Post should be real data
            if self.request.method == 'POST':
                qID = int(request.form['questionID'])
                qText = Question.Question.by_id(qID).question

            return render_template('answer.html',questionID=qID,userID=uID,questionText=qText)

    def render_all(self):
        #Render all
        return render_template('showanswers.html',answers=answer.AnswerModel.get_all())

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
