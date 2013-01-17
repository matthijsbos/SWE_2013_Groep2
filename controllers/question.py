import json
from flask import escape, render_template, g

from dbconnection import session
from models.question import Question


class QuestionController():
    @staticmethod
    def toggle_question(q_id):
        available = Question.by_id(q_id).available
        if g.lti.is_instructor():
            if available == True:
                Question.by_id(q_id).available = False
                return json.dump({"toggle": Frue,"check": True})
            else:
                Question.by_id(q_id).available = True
                return json.dump({"toggle": True,"check": True})
        else:
          return json.dump({"toggle": True,"check": False})
                
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
        session.add(Question("teacher1", "bla", "q1?", False,30))
        session.commit()
        return render_template('question_list.html',
                               questions=QuestionController.get_questions(30))

    @staticmethod
    def delete_question(qid):
        question = Question.by_id(int(qid))
        if g.lti.is_instructor():
            session.delete(question)
            session.commit()

        return json.dumps({'deleted': g.lti.is_instructor()})

    @staticmethod
    def ask_question(instructor):
        return render_template('askQuestion.html', instr=instructor)

    @staticmethod
    def create_question(question, instructor, course, time):
        try:
            time = int(time)
        except ValueError:
            time = 0
        session.add(Question(instructor, course, question, False, time))
        session.commit()

        return render_template('handleQuestion.html', question=question)
