import json
from flask import g
from dbconnection import session
from utilities import render_template
from models.answer import *
from models.review import * 
from clusterer import *

class Review_stats():
  @staticmethod
  def run(self,qid):
    answers=AnswerModel.get_question_answers(qid).all()
    clusterer=ClustererStars()
    data_set=[]
    output=[]
    best_avg_nr=0
    best_avg=0
    worst_avg_nr=0
    worst_avg=9999999999
    biggest_nr=0
    biggest=0
    for answer in answers:
      answer_text=answer.text
      average_stars=0
      nr_reviews=0
      star_total=0
      reviews=Review.get_list(answer.id)
      for review in reviews:
        star_total += review.rating
        nr_reviews += 1
      if nr_reviews > 0:
        average_stars=star_total/float(nr_reviews)
      else:
        average_stars=-1
      clusterer.add_answer(answer_text,average_stars)
    data_set=clusterer.run_clustering()
    for i in range(len(data_set)):
      if data_set[i][4] > biggest:
        biggest=data_set[i][4]
        biggest_nr=i
      if data_set[i][5] > best_avg:
        best_avg=data_set[i][5]
        best_avg_nr=i
      if data_set[i][5] < worst_avg:
        worst_avg=data_set[i][5]
        worst_avg_nr=i
      
    output.append(data_set[biggest_nr])
    output.append(data_set[best_avg_nr])
    output.append(data_set[worst_avg_nr])
    
    return output
      
  def render(self,qid):
    return render_template('review_stat.html',data_set=self.run(self,qid))