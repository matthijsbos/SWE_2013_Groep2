# Author :      Matthijs Bos
# Description:  Writes an answer choice to the database 

from flask import render_template, request, g
from models.answerchoice import AnswerChoiceModel
from dbconnection import session

class SaveAnswerChoice():
    def __init__(self, request):
        pass
    def process(self):
        userid = g.lti.get_user_id()
        try:
            answer0 = int(request.values['answerzero'])
        except KeyError:
            #TODO 
            pass

        try:
            answer1 = int(request.values['answerone'])
        except KeyError:
            #TODO
            pass
        
        try:
            bestanswer = int(request.values['bestanswer'])
        except KeyError:
            #TODO
            pass

        if answer0 == bestanswer:
            session.add(AnswerChoiceModel(userid,answer0,answer1))
            #TODO
            pass
        elif answer1 == bestanswer:
            session.add(AnswerChoiceModel(userid,answer1,answer0))
            #TODO
            pass
        else:
            #TODO 
            pass
