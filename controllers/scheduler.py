# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 16:50:07 2013

@author: Mustafa Karaalioglu
"""
from models.answer import AnswerModel
from models.schedule import Schedule


class Scheduler():
    def __init__(self, question_id):
        schedule_list = []
        user_list = []
        scores = []
        
        answers = AnswerModel.get_question_answers(question_id)
        for a in answers:
            scores.append((a.get_rating(), a))
            user_list.append(a.userID)
            
        scores.sort(key=lambda tup: tup[0])
        
        # TODO: possibly change fixed percentage to variable
        # IMPORTANT: users that did not give an answer should be able to rate,
        # not sure if that will happen right now
        #
        # initial scheduler
        shift_count = len(scores) - max(1, int(len(scores) * 0.2))
        user_list = user_list[shift_count:] + user_list[0:shift_count]
        
        for x in xrange(0, len(scores)):
            a_id = scores[x][1].id
            u_id = user_list[x]
            schedule_list.append(a_id, u_id)
        
        Schedule.add_list(schedule_list)
            