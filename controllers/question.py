from flask import render_template, g
from models.Question import Question
from dbconnection import session
from flask import escape


class questionController():
    def __init__(self):
        # create a few database items
        for model in session.query(Question):
            break
        else:
            session.add(Question("teacher1", "bla", "q1?", False, 0))
            session.add(Question("teacher1", "bla", "Hoe gaat het?", False, 0))
            session.add(Question("teacher1", "bla", "Hoe oud ben je?", False, 0))
            session.add(Question("teacher1", "bla", "Hoe heet je?", False, 0))
            session.add(Question("teacher1", "bla", "1337?", False, 0))
            session.commit()

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
        return Question.by_course_id(course_id)

    def render(self):
        self.editQuestion(1, "Ben ik nu een echte vraag?", True)
        return render_template('question.html',wordlist=self.getQuestion(4))

    @staticmethod
    def delete_question(qid):
        question = Question.by_id(int(qid))
        if g.lti.is_instructor():
            session.delete(question)
            session.commit()
            return render_template('deleteQuestion.html',
                    question = question,
                    permission = True)
        else:
            return render_template('deleteQuestion.html',
                    question = question,
                    permission = False)

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
