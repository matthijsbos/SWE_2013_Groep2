import json
from flask import escape, render_template, g

from dbconnection import Session
from models.question import Question

session = Session()


class QuestionController():
    #function that updates the question in the db
    @staticmethod
    def edit_question(q_id, question, activate):
        if question != None:
          escaped_question = escape(question)
          Question.by_id(q_id).question = question
        else:
          escaped_question = None
        Question.by_id(q_id).available = activate
        return json.dumps({"id":q_id,"text":escaped_question,"available":activate})

    #function to get the first n questions
    @staticmethod
    def get_questions(n):
        return session.query(Question).order_by(Question.available.desc())[:n]

    @staticmethod
    def export_course(course_id):
        questions = Question.by_course_id(course_id)
        return [{'question': question.question} for question in questions]

    @staticmethod
    def get_list():
        # TODO: pagination, etc..... same goes for get_questions
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
        return render_template('askQuestion.html',instr=instructor)

    @staticmethod
    def create_question(question, instructor, course, time):
        if not isinstance(time, (int, long)):
            time = 0
        session.add(Question(instructor, course, question, False, time))
        session.commit()

        return render_template('handleQuestion.html',question=question)
