import json
from flask import g
from utilities import render_template
from models.answer import AnswerModel
from models.question import UserQuestion
from models.user import UserModel


class Index():
    def __init__(self, debug=False):
        self.debug = debug

    def render(self):
        if self.debug:
            return render_template('index_debug.html',
                                   lti_dump=g.lti.dump_all())
        if g.lti.is_instructor():
            return render_template('index_instructor.html')
        else:
            print g.lti.get_user_name()
            UserModel.save(g.lti.get_user_id(), g.lti.get_user_name())

        return render_template('index_student.html')

    def has_new_question(self):
        questions = AnswerModel.get_active_questions(g.lti.get_user_id(),
                                                    g.lti.get_course_id())

        if len(questions) == 0:
            return json.dumps({'has_new': False})
        
        output = { 'has_new': True, 'len': len(questions) } 
        array = []        
        
        for question in questions:        
            time_remaining = question.get_time_left()
            
            answer_text = ''
            if AnswerModel.check_answer_exists(g.lti.get_user_id(), question.id) == 1:
                answer_text = AnswerModel.by_id(AnswerModel.get_answer_id(g.lti.get_user_id(), question.id)).text
            
            object = {'question_id': question.id,
                      'question_text': question.question,
                      'time_remaining': time_remaining,
                      'question_time': question.time,
                      'answer':answer_text}        
                      
            array.append(object)
                
        output['questions'] = array
        
        return json.dumps(output)

    def student_question(self, request):
        if g.lti.is_instructor():
            rv = []
            user_questions = UserQuestion.get_list(5)
            for q in user_questions:
                user = UserModel.by_user_id(q.user_id)
                if user is not None:
                    rv.append({'user':user.username, 'text':q.text, 'id':q.id})
        else:
            rv = dict({'error': True, 'type': ''})
            try:
                text = request.form['text']
            except KeyError:
                rv['type'] = 'key'
                return json.dumps(rv)
            
            min_delay = 10
            dt = UserQuestion.time_since_last(g.lti.get_user_id())
            if dt is not None and dt < min_delay:
                rv['type'] = 'time'
            else:
                rv['error'] = False
                UserQuestion.add(g.lti.get_user_id(), text)
        
        return json.dumps(rv)