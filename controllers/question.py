from flask import render_template, g
from models.Question import Question
from dbconnection import session
from flask import escape


class questionController():
    #function that updates the question in the db
    @staticmethod
    def editQuestion(q_id, question, activate):
        escaped_question = escape(question)
        Question.by_id(q_id).question = question
        Question.by_id(q_id).available = activate

    #function to get the first n questions
    @staticmethod
    def getQuestion(n):
        return session.query(Question).order_by(Question.modified.desc())[:n]

    @staticmethod
    def exportCourse(course_id):
        questions = Question.by_course_id(course_id)
        return [{'question': question.question} for question in questions]

    @staticmethod
    def delete_question(qid):
        question = Question.by_id(int(qid))
        if g.lti.is_instructor():
            session.delete(question)
            session.commit()

        return render_template('deleteQuestion.html',
                question = question,
                permission = g.lti.is_instructor())

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
