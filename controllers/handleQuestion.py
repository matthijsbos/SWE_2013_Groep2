# Author: Daniel Sepers
# Description: This file handles inserting the received question into a database
from flask import render_template

class HandleQuestion():
    question = ""
    
    def __init__(self):
        self.question = ""

    def add_question(self,question):
        self.question = question
        # insert question into database here
    
    def render(self):
        return render_template('handleQuestion.html',question=self.question)
