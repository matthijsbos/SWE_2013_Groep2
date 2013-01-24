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
import json


class ReviewAnswer():
    def __init__(self, request):
        """
        Handle the reviewed answer
        """
        try:
            fsession['reviewanswer']
        except:
            return None

        #for rating in request.form.getlist('rating'):
        #    Review.add(fsession['reviewanswer'], fsession['user_id'], rating, )
            
        for review in request.form.getlist('comments'):
            rating = request.form['rating']
            if review is not '':
                Review.add(fsession['reviewanswer'], fsession['user_id'], rating,
                            review)
            else:
                Review.add(fsession['reviewanswer'], fsession['user_id'], rating,
                '')

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
    def review(answer_id):
        # one of these checks can be removed once we merge and know what's what
        try:
            answer = AnswerModel.by_id(answer_id)
        except:
			return render_template('reviewanswer.html', error="true")
            #return "<div class=\"alert alert-error\"><i class=\"icon-warning-sign\"></i>No answers found!</div>"
        if answer == None:
			return render_template('reviewanswer.html', error="true")
            #return "<div class=\"alert alert-error\"><i class=\"icon-warning-sign\"></i>No answers found!</div>"
        try:
            question = Question.by_id(answer.questionID)
        except:
            return "Error question not found"
            

        fsession['reviewanswer'] = answer_id

        enabledtags = AnswerTag.get_tag_ids(answer_id)

        return render_template('reviewanswer.html', answer=answer,
                               tags=Tag.get_all(), enabledtags=enabledtags,
                               tagsOn = question.tags, commentOn = question.comment,
                               ratingOn = question.rating)

    """
    Stub class, to be implemented by mustafa
    """
    @staticmethod 
    def has_new_review():
        if g.lti.is_instructor():
            return json.dumps({'has_new': False})

        return json.dumps({'has_new': True,
                           'number': 5 })
