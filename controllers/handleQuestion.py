# Author: Daniel Sepers
# Description: This file handles inserting the received question into a database
from flask import render_template
from dbconnection import session
from models.Question import Question

class HandleQuestion():
    question = ""
    
    def __init__(self):
        self.question = ""

    def add_question(self,question):
        self.question = question
        session.add(Question("teacher1", "", question, False))
        session.commit()
    
    def render(self):
        return render_template('handleQuestion.html',question=self.question)
