# Author: Daniel Sepers
# Description: This file handles the input page for an instructor's question
from flask import render_template

class AskQuestion():
    instructor = ""
    
    def __init__(self):
        self.instructor = ""
        
    def set_instructor(self,instr):
        self.instructor = instr


    def render(self):
        return render_template('askQuestion.html',instr=self.instructor)
