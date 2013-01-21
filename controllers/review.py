# Authors : Victor Azizi & David Schoorisse & Mustafa Karaalioglu
# Descrp : Controls the reviewing of answers
# Changes:
# Comment: call ReviewAnswer.review(x) to start reviewing a answer

from flask import render_template, session as fsession
from models.tag import Tag, AnswerTag
from models.answer import AnswerModel
from models.rating import AnswerRating, Rating
from models.comment import Comment
from dbconnection import Session

session = Session()

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

        for rating_id in request.form.getlist('rating'):
            AnswerRating.add_answerrating(fsession['reviewanswer'], rating_id)

        for tag_id in request.form.getlist('remove_tags'):
            AnswerTag.remove(fsession['reviewanswer'], tag_id)
            
        for comment in request.form.getlist('comments'):
            if comment is not '':
                Comment.add(fsession['reviewanswer'], fsession['user_id'], 
                            comment)

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
        
