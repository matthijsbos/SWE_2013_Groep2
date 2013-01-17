from flask import render_template, g


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

        # TODO: call function from question controller/model
        ids = Question.get_unanswered()
        question = Answer.get_id(ids[0])
        # TODO: send first unanswered
        return json.dumps({'has_new': True,
                           'question_id': question.id,
                           'question_text': question.question,
                           'time_remaining': question.time})
