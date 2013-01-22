import json
import time
from datetime import datetime, timedelta
from flask import render_template, g

from models.answer import AnswerModel
from controllers.answer import Answer


class Index():
    def __init__(self, debug=False):
        self.debug = debug

    def render(self):
        if self.debug:
            return render_template('index_debug.html',
                                   lti_dump=g.lti.dump_all())
        if g.lti.is_instructor():
            return render_template('index_instructor.html')

        return render_template('index_student.html', unansq_questions = AnswerModel.get_unanswered_questions(g.lti.get_user_id(),
                                                    g.lti.get_course_id()), answ_questions = AnswerModel.get_answered_active_questions(g.lti.get_user_id(),
                                                    g.lti.get_course_id()))

    def has_new_question(self):
        if g.lti.is_instructor():
            return json.dumps({'has_new': False})

        question = AnswerModel.get_unanswered_questions(g.lti.get_user_id(),
                                                    g.lti.get_course_id())

        if not len(question):
            return json.dumps({'has_new': False})

        question = question[0]

        time_remaining = datetime.now() - (question.modified +
                timedelta(seconds=question.time))
        time_remaining = time_remaining.seconds + time_remaining.days * 86400
        time_remaining = -time_remaining

        return json.dumps({'has_new': True,
                           'question_id': question.id,
                           'question_text': question.question,
                           'time_remaining': time_remaining})

    def answer_it(question_id):
        return render_template('student_answer.html')