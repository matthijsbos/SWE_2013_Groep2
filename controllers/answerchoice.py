# Author : Diederik Beker
# Descrp : Contains controller logic for the answer choice
# Changes:
# Comment:

from flask import render_template, g
from models.question import Question
from models.answer import AnswerModel
from models import answer
from dbconnection import session
from random import choice

class Answerchoice():
	def __init__(self, request):		
		# lele add dummy questions le
		if len(Question.get_all()) == 0:
			userID = g.lti.get_user_id()
			q1 = Question("1","1","What am I?",True)
			q2 = Question("2","1","Who am I?",True)
			q3 = Question("3","1","Where am I?",True)
			session.add(q1)
			session.add(q2)
			session.add(q3)
			a11 = AnswerModel("einseins",1,userID,0)
			a12 = AnswerModel("einszwei",1,1338,0)
			a13 = AnswerModel("einsdrei",1,1339,0)
			a21 = AnswerModel("zweieins",2,userID,0)
			a22 = AnswerModel("zweizwei",2,1338,0)
			a23 = AnswerModel("zweidrei",2,1339,0)
			a31 = AnswerModel("dreieins",3,userID,0)
			a32 = AnswerModel("dreizwei",3,1338,0)
			a33 = AnswerModel("dreidrei",3,1339,0)
			session.add(a11)
			session.add(a12)
			session.add(a13)
			session.add(a21)
			session.add(a22)
			session.add(a23)
			session.add(a31)
			session.add(a32)
			session.add(a33)
			session.commit()

	def render(self):
		userID = g.lti.get_user_id()
		questionID = 1
		allquestions = (Question.get_all())
		#print allquestions
		allanswers = (AnswerModel.get_all())
		#print allanswers
		validAnswers = []
		for current in allanswers:
			if current.userID != userID and current.questionID == questionID:
				#print current.userID
				#print userID
				validAnswers.append(current)
		print validAnswers
		return render_template('choice.html',questions=allquestions[0], answers=choice(validAnswers))