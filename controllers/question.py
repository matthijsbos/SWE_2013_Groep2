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
            session.add(Question("teacher1", "bla", "q1?", False))
            session.add(Question("teacher1", "bla", "Hoe gaat het?", False))
            session.add(Question("teacher1", "bla", "Hoe oud ben je?", False))
            session.add(Question("teacher1", "bla", "Hoe heet je?", False))
            session.add(Question("teacher1", "bla", "1337?", False))
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
            session.expunge(question)
            session.commit()
            return render_template('deleteQuestion.html',
                    question = question,
                    permission = True)
        else:
            return render_template('deleteQuestion.html',
                    question = question,
                    permission = False)

    @staticmethod
    def ask_question(self, instructor):
        return render_template('askQuestion.html',instr=self.instructor)


class HandleQuestion():
    question = ""
    time = 0

    def __init__(self):
        self.question = ""

    def add_question(self,question):
        self.question = question
        session.add(Question("teacher1", "", question, False))
        session.commit()

    def set_time(self,time):
        if isinstance(time,(int,long)):
          self.time = time

    def render(self):
        return render_template('handleQuestion.html',question=self.question)
