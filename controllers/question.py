import json
from flask import escape, render_template, g

from dbconnection import session
from models.question import Question
from controllers.scheduler import Scheduler


class QuestionController():
    @staticmethod
    def toggle_question(q_id):
        '''toggles a question between available and not available'''
        if g.lti.is_instructor():
            available = Question.toggle_available(q_id)
            return json.dumps({"toggle":available,"check": True})

        else:
          return json.dumps({"toggle": True,"check": False})

    @staticmethod
    def availability(args):
        """
        Handles availability via the question_list form
        """
        try:
            question = Question.by_id(args['id'])
        except KeyError:
            return 

        if not g.lti.is_instructor():
            return

        try:
            t = args['type']
        except KeyError:
            return 
        
        if t == 'answerable':
            question.answeravailable = not question.answeravailable

        elif t == 'reviewable':
            question.reviewavailable = not question.reviewavailable

        elif t == 'archived':
            question.archived = not question.archived

        if question.reviewavailable:
            Scheduler(args['id'])
            
        return json.dumps({"answerable": question.answeravailable,
                           "reviewable": question.reviewavailable,
                           "archived"  : question.archived,
                           "check"     : True,
                         })

    @staticmethod
    def edit_question(q_id, question, activate):
        """Updates a question with given contents and activation status."""
        if g.lti.is_instructor():
            if question != None:
                escaped_question = escape(question)
                Question.by_id(q_id).question = question
            else:
                escaped_question = None
            Question.by_id(q_id).available = activate
            return json.dumps({"id": q_id,
                               "text": escaped_question,
                               "available": activate,
                               "check": g.lti.is_instructor()})
        else:
            return json.dumps({"id": q_id,
                               "text": question,
                               "available": activate,
                               "check": g.lti.is_instructor()})

    @staticmethod
    def get_questions(n):
        """Retrieves the first n questions, sorted by date available."""
        return session.query(Question).order_by(Question.available.desc())[:n]

    @staticmethod
    def export_course(course_id):
        questions = Question.by_course_id(course_id)
        return [{'question': question.question} for question in questions]
    
    @staticmethod
    def get_list_asked():
       """Retrieves questions asked by the user currently logged in."""
       if g.lti.is_instructor():
           # TODO: pagination, etc..... same goes for get_questions
           session.commit()
           return render_template('question_list.html',
                                  questions=session.query(Question).filter_by(user_id=g.lti.get_user_id()  ) )
       else:
           session.commit()
           return render_template('question_list.html',
                                  questions=session.query(Question).filter_by(user_id=g.lti.get_user_id()  ) )

    @staticmethod
    def get_list_to_answer():
     """Retrieves questions to be answered by the instructor (all questions )"""
     if g.lti.is_instructor():
         # TODO: pagination, etc..... same goes for get_questions
         session.commit()
         return render_template('answer_student_questions.html',
                                questions=session.query(Question).\
                                    filter(Question.course_id == g.lti.get_course_id() ).\
                                    filter(Question.course_id != g.lti.get_user_id() ))         #Filter questions by instructor                                    

     #Only instructors can answer these questions
     else:
         return render_template('access_restricted.html')
        

    @staticmethod
    def delete_question(qid):
        '''removes the question with the provided id from the database'''
        question = Question.by_id(int(qid))
        if g.lti.is_instructor():
            session.delete(question)
            session.commit()

        return json.dumps({'deleted': g.lti.is_instructor()})

    @staticmethod
    def ask_question(instructor):
        '''passes the name of the course instructor to the ask question module and calls the screen to ask a question'''
        return render_template('askQuestion.html', instr=instructor)

    @staticmethod
    def create_question(question, instructor, course, active, time):
        '''formats a question for database insertion and inserts it, calls a result screen afterwards'''
        try:
            time = int(time)
        except ValueError:
            time = 0
        session.add(Question(instructor, course, question, active, time))
        session.commit()

        return QuestionController.get_list_asked()
