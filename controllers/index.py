import json
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

        return render_template('index_student.html')

    def has_new_question(self):
        if g.lti.is_instructor():
            return json.dumps({'has_new': False})

        answers = AnswerModel()
        question = answers.get_unanswered_questions(g.lti.get_user_id(),
                                                    g.lti.get_course_id())

        if not len(question):
            return json.dumps({'has_new': False})

        question = question[0]

        # HACK: call answerQuestion to generate an empty record, so saving
        # itself doesn't crash... TODO?
        answer_ctrler = Answer(None)
        answer_ctrler.answerQuestion(g.lti.get_user_id(), question.id,
                question.question, question.time)

        return json.dumps({'has_new': True,
                           'question_id': question.id,
                           'question_text': question.question,
                           'time_remaining': question.time})
