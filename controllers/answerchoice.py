# Author : Diederik Beker
# Descrp : Contains controller logic for the answer choice
# Changes:
# Comment:

from flask import render_template, g, request
from models.question import Question
from models.answer import AnswerModel
from models.answerchoice import AnswerChoiceModel
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
            return 404
        except ValueError:
            return 404

        try:
            answer1 = int(request.values['answerone'])
        except KeyError:
            return 404
        except ValueError:
            return 404
        
        try:
            bestanswer = int(request.values['bestanswer'])
        except KeyError:
            return 404
        except ValueError:
            return 404

        print userid

        if answer0 == bestanswer:
            best = answer0
            other = answer1
        elif answer1 == bestanswer:
            best = answer1
            other = answer0
        else:
            return 404
        
        print best
        print other

        #try:
        session.add(AnswerChoiceModel(userid,best,other))
        session.commit()
        #except:
        #    print 'error in SQL'
        #    session.rollback()

        return str(len(AnswerChoiceModel.get_all()))
