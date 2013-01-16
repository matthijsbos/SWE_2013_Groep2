# Author : Diederik Beker
# Descrp : Contains controller logic for the answer choice
# Changes:
# Comment:

from flask import render_template
from models.question import Question
from models.answer import AnswerModel
from models import answer
from dbconnection import session

class Answerchoice():
    def __init__(self, request):
		
		session.add(Question("1","1","What am I?",True))
		session.add(Question("2","1","Who am I?",True))
		session.add(Question("3","1","Where am I?",True))
		session.commit()

    def render(self):
        return render_template('choice.html',questions=Question.by_id(1), answers=AnswerModel.by_id(1))
