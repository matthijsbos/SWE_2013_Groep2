# Author: Arjen Tamerus
# Description: Delete selected questions
from flask import render_template, g
from dbconnection import session
from models.Question import Question

class DeleteQuestion():

  def __init__(self, qid):
    for model in session.query(Question):
      break
    else:
      session.add(Question("aTeacer", "bla0", "questionToDelte", False))
      session.add(Question("aTeacer", "bla1", "questionToDelte", False))
      session.add(Question("aTeacer", "bla2", "questionToDelte", False))
      session.add(Question("aTeacer", "bla3", "questionToDelte", False))
      session.add(Question("aTeacer", "bla4", "questionToDelte", False))
      session.commit()

    self.question = Question.by_id(int(qid))

  def delete_question(self):
    if g.lti.is_instructor():
      session.expunge(self.question)
      session.commit()

  def render(self):
    if g.lti.is_instructor():
      return render_template('deleteQuestion.html', question = self.question, permission = True)
    else:
      return render_template('deleteQuestion.html', question = self.question, permission = False)
