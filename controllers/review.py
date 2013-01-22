# Authors : Victor Azizi & David Schoorisse & Mustafa Karaalioglu
# Descrp : Controls the reviewing of answers
# Changes:
# Comment: call ReviewAnswer.review(x) to start reviewing a answer

from flask import render_template, g, session as fsession
from models.tag import Tag, AnswerTag
from models.answer import AnswerModel
from models.review import Review
from models.comment import Comment
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
            return self

        for tag_id in request.form.getlist('assign_tags'):
            AnswerTag.add_answertag(fsession['reviewanswer'], tag_id)

        #for rating in request.form.getlist('rating'):
        #    Review.add(fsession['reviewanswer'], fsession['user_id'], rating, )

        for tag_id in request.form.getlist('remove_tags'):
            AnswerTag.remove(fsession['reviewanswer'], tag_id)
            
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
    def review(answer_id):

        # one of these checks can be removed once we merge and know what's what
        try:
            answer = AnswerModel.by_id(answer_id)
        except:
            return "Error answer not found"
        if answer == None:
            return "Error answer not found"

        fsession['reviewanswer'] = answer_id

        enabledtags = AnswerTag.get_tag_ids(answer_id)

        return render_template('reviewanswer.html', answer=answer,
                               tags=Tag.get_all(), enabledtags=enabledtags)

    """
    Stub class, to be implemented by mustafa
    """
    @staticmethod 
    def has_new_review():
        if g.lti.is_instructor():
            return json.dumps({'has_new': False})

        return json.dumps({'has_new': True,
                           'number': 5 })
