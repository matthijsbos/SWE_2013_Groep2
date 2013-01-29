# Authors : Victor Azizi & David Schoorisse & Mustafa Karaalioglu
# Descrp : Controls the reviewing of answers
# Changes:
# Comment: call ReviewAnswer.review(x) to start reviewing a answer

from flask import g, session as fsession
from utilities import render_template
from models.tag import Tag, AnswerTag
from models.answer import AnswerModel
from models.review import Review
from models.question import Question
from dbconnection import session
from models.schedule import Schedule
from controllers.question import QuestionController
from controllers.answer import Answer as AnswerController
import json


class ReviewAnswer():
    def __init__(self, request):
        """
        Handle the reviewed answer
        """
        try:
            fsession['reviewanswer']
        except:
            pass
        else:
            # for rating in request.form.getlist('rating'):
            # Review.add(fsession['reviewanswer'], fsession['user_id'], rating, )
    
            for tag_id in request.form.getlist('remove_tags'):
                AnswerTag.remove(fsession['reviewanswer'], tag_id)
            
            try:
                request.form['rating']
            except KeyError:
                pass
            else:
                Review.add(fsession['reviewanswer'], g.lti.get_user_id(),
                           request.form['rating'], request.form['comments'])
                           
                # users can review only once per answer so delete from schdule list
                Schedule.delete(fsession['reviewanswer'], g.lti.get_user_id())
                                   
            # revoke permission to review answer
            del fsession['reviewanswer']
    
    @staticmethod
    def remove_tag_answer(aid, tagid):
        AnswerTag.remove(aid, tagid)
        return json.dumps({'deleted': True})

    @staticmethod
    def add_tag_answer(aid, tagid):
        AnswerTag.add_answertag(aid, tagid)
        return json.dumps({'deleted': True})
    
    
    @staticmethod
    def review():
        answer = Schedule.get_answer(g.lti.get_user_id())
        if answer == None:
            return "No answers to review."

        fsession['reviewanswer'] = answer.id

        enabledtags = AnswerTag.get_tag_ids(answer.id)
        reviews = Review.get_list(answer.id)

        return render_template('reviewanswer.html', answer=answer,
                               tags=Tag.get_all(), enabledtags=enabledtags,
                               reviews=reviews)

    @staticmethod
    def start_review(request):
        try:
            question_id = request.form['question_id']
        except:
            return json.dumps({'reviewable':False})
        
        question = Question.by_id(question_id)
        reviewable = False
        if question is not None:
            if g.lti.is_instructor() or \
                    (question.get_time_left() <= 0 and question.time > 0):
                reviewable = QuestionController.availability(
                {'id':question_id, 'type':'reviewable'})
            
        return json.dumps({'reviewable':reviewable})
        
    @staticmethod 
    def has_new_review():
        answer = Schedule.get_answer(g.lti.get_user_id())
        
        if g.lti.is_instructor() or answer is None:
            return json.dumps({'has_new': False})

        return json.dumps({'has_new': True})
