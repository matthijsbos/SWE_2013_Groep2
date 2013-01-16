from flask import render_template
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

    def render(self):
        self.editQuestion(1, "Ben ik nu een echte vraag?", True)
        return render_template('question.html',wordlist=self.getQuestion(4))
