import json
import time
from datetime import datetime, timedelta
from flask import g
from utilities import render_template
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
        questions = answers.get_unanswered_questions(g.lti.get_user_id(),
                                                    g.lti.get_course_id())

        if len(questions) == 0:
            return json.dumps({'has_new': False})
        
        output = { 'has_new': True, 'len': len(questions) } 
        array = []        
        
        for question in questions:        
            time_remaining = datetime.now() - (question.activate_time +
                    timedelta(seconds=question.time))
            time_remaining = time_remaining.seconds + time_remaining.days * 86400
            time_remaining = -time_remaining      
            
            object = {'question_id': question.id,
                      'question_text': question.question,
                      'time_remaining': time_remaining,
                      'question_time': question.time}        
                      
            array.append(object)
        
        #qArray = {'questions': array}        
        output['questions'] = array
        
        return json.dumps(output)
