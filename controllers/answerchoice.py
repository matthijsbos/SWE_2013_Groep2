# Author : Diederik Beker
# Descrp : Contains controller logic for the answer choice
# Changes:
# Comment:

from flask import g, request, abort, redirect
from models.question import Question
from models.answer import AnswerModel
from models.answerchoice import AnswerChoiceModel
from models import answer
from dbconnection import session
from random import randrange
from collections import Counter
from utilities import render_template

class Answerchoice():
    def __init__(self, request):        
        pass
    
    def render(self):
        try:
            questionid = int(request.values['questionid'])
            answerid1 = int(request.values['answerid1'])
            answerid2 = int(request.values['answerid2'])
        except:
            return abort(404)
            
        try:
            question = Question.by_id(questionid)
            answer1 = AnswerModel.by_id(answerid1)
            answer2 = AnswerModel.by_id(answerid2)
        except:
            return abort(404)
            
        if AnswerModel.question_valid(questionid):
            return render_template('choice.html',
                                   question = question,
                                   answer1 = answer1,
                                   answer2 = answer2)
        else:
            return redirect('/choicelobby?question_id=' + questionid)
    
    def process(self):
        userid = g.lti.get_user_id()

        try:
            answer0 = int(request.values['answerzero'])
            answer1 = int(request.values['answerone'])
            bestanswer = int(request.values['bestanswer'])
        except KeyError:
            return abort(404)
        except ValueError:
            return abort(404)
        
        if answer0 == bestanswer:
            best  = answer0
            other = answer1
        elif answer1 == bestanswer:
            best  = answer1
            other = answer0
        else:
            return abort(404)

        #try:
        session.add(AnswerChoiceModel(userid,best,other))
        session.commit()
        #except:
        #    session.rollback()

        return redirect('/')
        #return render_template('index_student.html', unansq_questions = AnswerModel.get_unanswered_questions(g.lti.get_user_id(),
        #                                            g.lti.get_course_id()), answ_questions = AnswerModel.get_answered_active_questions(g.lti.get_user_id(),
        #                                            g.lti.get_course_id())) 

    def lobby(self):
        def randpop(array):
            return array.pop(randrange(0,len(array)))
            
        def getotheranswers(userID,questionID):
            allanswers = (AnswerModel.get_all())
            allanswerchoices = (AnswerChoiceModel.get_all())
            validAnswers = []
            for currentanswer in allanswers:
                # if relevant answer and not submitted by the current user
                if currentanswer.userID != userID and currentanswer.questionID == questionID:
                    shouldadd = True
                    for currentanswerchoice in allanswerchoices:
                        # if answer was not rated before by the current user
                        if (currentanswerchoice.best_answer_id == currentanswer.id or currentanswerchoice.other_answer_id == currentanswer.id) and currentanswerchoice.user_id == userID:
                            break
                    else: validAnswers.append(currentanswer.id)
                
            return validAnswers
        
        def getuncommons(answers):
            answerchoices = (AnswerChoiceModel.get_all())
            cnt = Counter()
            for answer in answers:
                cnt[answer] = 0
            for answerchoice in answerchoices:
                if answerchoice.best_answer_id in answers:
                    cnt[answerchoice.best_answer_id] += 1
            
            if len(cnt) > 1:
                return [cnt.most_common()[-1][0],cnt.most_common()[-2][0]]
            else: return False

        userID = g.lti.get_user_id()
        questionID = int(request.values['question_id'])

        validAnswers = getotheranswers(userID,questionID)
        print validAnswers
        uncommons = getuncommons(validAnswers)
        print uncommons
        
        if uncommons == False:
            return render_template('choicelobby.html',question=questionID)
        else:
            #return redirect('/answerchoice?questionid='+str(questionID)+'&answerid1='+str(randpop(validAnswers))+'&answerid2='+str(randpop(validAnswers)))
            return redirect('/answerchoice?questionid='+str(questionID)+'&answerid1='+str(randpop(uncommons))+'&answerid2='+str(randpop(uncommons)))
