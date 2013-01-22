# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 16:50:07 2013

@author: Mustafa Karaalioglu
"""
from models.answer import AnswerModel
from models.schedule import Schedule


class Scheduler():
    def __init__(self, question_id):
        self.question_id = question_id
        
    def schdule(self):
        schedule_list = []
        user_list = []
        scores = []
        
        answers = AnswerModel.get_question_answers(self.question_id)
        for a in answers:
            scores.append((a.get_rating(), a))
            user_list.append(a.userID)
            
        scores.sort(key=lambda tup: tup[0])
        
        # TODO: user sorting based on rating
        
        for x in xrange(0, len(scores)):
            a_id = scores[x][1].id
            u_id = user_list[x]
            schedule_list.append(a_id, u_id)
        
        Schedule.add_list(schedule_list)
            