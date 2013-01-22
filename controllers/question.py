import json
from flask import escape, render_template, g

from dbconnection import session
from models.question import Question


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
    def ask_question(user):
        '''passes the name of the course instructor to the ask question module and calls the screen to ask a question'''
        if g.lti.is_instructor():
            return render_template('askQuestion.html', instr=user)

        else:
            return render_template('askUserQuestion.html', stud=user, course=g.lti.get_course_id(),)
            
    @staticmethod
    def create_question(question, instructor, course, active, time):
        '''formats a question for database insertion and inserts it, calls a result screen afterwards'''
        try:
            time = int(time)
        except ValueError:
            time = 0
        session.add(Question(instructor, course, question, active, time))
        session.commit()

        return QuestionController.get_list()
