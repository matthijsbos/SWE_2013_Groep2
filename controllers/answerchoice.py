# Author : Diederik Beker
# Descrp : Contains controller logic for the answer choice
# Changes:
# Comment:

from flask import render_template, g, request
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
        print 'render'
        return render_template('choice.html',questions=Question.by_id(1), answers=answer.AnswerModel.by_id(1))

    def process(self):
        userid = g.lti.get_user_id()
        try:
            answer0 = int(request.values['answerzero'])
        except KeyError:
            #TODO 
            return ''

        try:
            answer1 = int(request.values['answerone'])
        except KeyError:
            #TODO
            return ''
        
        try:
            bestanswer = int(request.values['bestanswer'])
        except KeyError:
            #TODO
            return ''

        if answer0 == bestanswer:
            #session.add(AnswerChoiceModel(userid,answer0,answer1))
            #TODO
            pass
        elif answer1 == bestanswer:
            #session.add(AnswerChoiceModel(userid,answer1,answer0))
            #TODO
            pass
        else:
            #TODO 
            pass
