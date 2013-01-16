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

    def render(self):
        self.editQuestion(1, "Ben ik nu een echte vraag?", True)
        return render_template('question.html',wordlist=self.getQuestion(4))

class AskQuestion():
    instructor = ""
    
    def __init__(self):
        self.instructor = ""
        
    def set_instructor(self,instr):
        self.instructor = instr


    def render(self):
        return render_template('askQuestion.html',instr=self.instructor)

class HandleQuestion():
    question = ""
    instructor = ""
    course = ""
    time = 0
    
    def __init__(self):
        self.question = ""
        self.time = 0
        self.instuctor = ""
        self.course = ""

    def add_question(self,question):
        self.question = question
        session.add(Question(self.instructor, self.course, question, False, self.time))
        session.commit()
        
    def set_time(self,time):
        if isinstance(time,(int,long)):
            self.time = time
          
    def set_course(self,course):
        self.course = course
        
    def set_instructor(self,instructor):
        self.instructor = instructor
    
    def render(self):
        return render_template('handleQuestion.html',question=self.question)
