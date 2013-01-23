import json
from flask import escape, g
from utilities import render_template
from dbconnection import session
from models.question import Question
from datetime import datetime, timedelta

class QuestionController():
    @staticmethod
    def toggle_question(q_id, field):
        '''toggles a question between available and not available'''
        if g.lti.is_instructor():
            available = Question.toggle_available(q_id, field)
            return json.dumps({"toggle":available,"check": True})

        else:
          return json.dumps({"toggle": True,"check": False})

    @staticmethod
    def edit_question(q_id, question, time):
        """Updates a question with given contents and activation status."""
        if g.lti.is_instructor():
            if question is None:
                escaped_question = None
            else:
                escaped_question = escape(question)

            escaped_time = escape(time)
            q = Question.by_id(q_id)
            q.question = escaped_question
            q.time = int(time)
            activate = q.available

            session.add(q)
            session.commit()

            return json.dumps({"id": q_id,
                               "text": escaped_question,
                               "available": activate,
                               "time":time,
                               "check": g.lti.is_instructor()})
        else:
            return json.dumps({"id": q_id,
                               "text": question,
                               "available": activate,
                               "time": time,
                               "check": g.lti.is_instructor()})
    
    @staticmethod
    def get_remaining_time(q_id):
        question = Question.by_id(q_id)
        
        if question is not None and question.activate_time is not None:
            time_remaining = QuestionController.calculate_remaining_time(question)
            question_time =  question.time
        else:
            time_remaining = 0
            question_time =  0
            
        return json.dumps({"still_available":((question is not None) and question.available),
                           "time_remaining":time_remaining,
                           "question_deleted":(question is None),
                           "question_time":question_time})

    @staticmethod
    def get_questions(n):
        """Retrieves the first n questions, sorted by date available."""
        return session.query(Question).order_by(Question.available.desc())[:n]

    @staticmethod
    def export_course(course_id):
        questions = Question.by_course_id(course_id)
        return [{'question': question.question} for question in questions]

    @staticmethod
    def get_list():
        # TODO: pagination, etc..... same goes for get_questions
        session.commit()
        return render_template('question_list.html',
                               questions=session.query(Question).order_by(Question.available.desc()))

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
    def create_question(question, instructor, course, active, time, comment, tags, rating):
        '''formats a question for database insertion and inserts it, calls a result screen afterwards'''
        try:
            time = int(time)
        except ValueError:
            time = 0
        session.add(Question(instructor, course, question, active, time, comment, tags, rating))
        session.commit()

        return QuestionController.get_list()
    
    @staticmethod
    def calculate_remaining_time(question):
        time_remaining = datetime.now() - (question.activate_time +
                timedelta(seconds=question.time))
        time_remaining = time_remaining.seconds + time_remaining.days * 86400
        return - time_remaining
