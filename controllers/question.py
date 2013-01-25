import json
from flask import escape, g
from utilities import render_template
from dbconnection import session
from models.question import Question
from datetime import datetime, timedelta
from controllers.scheduler import Scheduler


class QuestionController():
    @staticmethod
    def toggle_question(q_id, field):
        '''toggles a question between available and not available'''
        if g.lti.is_instructor():
            QuestionController.availability({'id':q_id,'type':'reviewable'})
            return json.dumps({"toggle":Question.by_id(q_id).reviewavailable,"check": True})

        else:
          return json.dumps({"toggle": True,"check": False})

    @staticmethod
    def availability(args):
        """
        Handles availability via the question_list form
        """
        try:
            question = Question.by_id(args['id'])
        except KeyError:
            return 

        if not g.lti.is_instructor():
            return

        try:
            t = args['type']
        except KeyError:
            return 
        
        if t == 'answerable':
            question.answeravailable = not question.answeravailable
            question.activate_time = datetime.now()

        elif t == 'reviewable':
            question.reviewavailable = not question.reviewavailable
            question.activate_time = datetime.now()
            if not question.reviewavailable:
                Scheduler(args['id'])

        elif t == 'archived':
            question.archived = not question.archived

        if question.reviewavailable:
            Scheduler(args['id'])
            
        return json.dumps({"answerable": question.answeravailable,
                           "reviewable": question.reviewavailable,
                           "archived"  : question.archived,
                           "check"     : True,
                         })

    @staticmethod
    def edit_question(q_id, question, time):
        """Updates a question with given contents and activation status."""
        if g.lti.is_instructor():
            if question is None:
                escaped_question = None
            else:
                escaped_question = escape(question)

            escaped_time = escape(time)
            q = Question.by_id(q_id)
            q.question = escaped_question
            q.time = int(time)
            activate = q.available

            session.add(q)
            session.commit()

            return json.dumps({"id": q_id,
                               "text": escaped_question,
                               "available": activate,
                               "time":time,
                               "check": g.lti.is_instructor()})
        else:
            return json.dumps({"id": q_id,
                               "text": question,
                               "available": activate,
                               "time": time,
                               "check": g.lti.is_instructor()})
    
    @staticmethod
    def get_remaining_time(q_id):
        question = Question.by_id(q_id)
        
        if question is not None and question.activate_time is not None:
            time_remaining = QuestionController.calculate_remaining_time(question)
            question_time =  question.time
        else:
            time_remaining = 0
            question_time =  0
            
        return json.dumps({"still_available":((question is not None) and question.reviewavailable),
                           "time_remaining":time_remaining,
                           "question_deleted":(question is None) or not question.reviewavailable,
                           "question_time":question_time})

    @staticmethod
    def get_questions(n):
        """Retrieves the first n questions, sorted by date available."""
        return session.query(Question).order_by(Question.available.desc())[:n]

    @staticmethod
    def export_course(course_id):
        questions = Question.by_course_id(course_id)
        return [{'question': question.question} for question in questions]
    
    @staticmethod
    def get_list_asked():
       """Retrieves questions asked by the user currently logged in."""
       if g.lti.is_instructor():
           # TODO: pagination, etc..... same goes for get_questions
           session.commit()
           return render_template('question_list.html',
                                  questions=session.query(Question).filter_by(user_id=g.lti.get_user_id()  ) )
       else:
           session.commit()
           return render_template('question_list.html',
                                  questions=session.query(Question).filter_by(user_id=g.lti.get_user_id()  ) )

    @staticmethod
    def get_list():
        questions = Question.get_filtered()
        for question in questions:
            if question is not None and question.activate_time is not None:
                if QuestionController.calculate_remaining_time(question) < 0:            
                    question.available = False
        session.commit()
        return render_template('question_list.html', questions=questions)

    @staticmethod
    def get_list_table(limit,offset):
        (questions, curpage, maxpages, startpage, pagecount) = Question.get_filtered_offset(limit,offset)
        for question in questions:
            if question is not None and question.activate_time is not None:
                if QuestionController.calculate_remaining_time(question) < 0:            
                    question.available = False
        session.commit()

        return render_template('question_list_tbl.html', questions=questions,
                currentpage=curpage,startpage=startpage,pagecount=pagecount,maxpages=maxpages)

    def get_list_to_answer():
     """Retrieves questions to be answered by the instructor (all questions )"""
     if g.lti.is_instructor():
         # TODO: pagination, etc..... same goes for get_questions
         session.commit()
         return render_template('answer_student_questions.html',
                                questions=session.query(Question).\
                                    filter(Question.course_id == g.lti.get_course_id() ).\
                                    filter(Question.course_id != g.lti.get_user_id() ))         #Filter questions by instructor                                    

     #Only instructors can answer these questions
     else:
         return render_template('access_restricted.html')
        

    @staticmethod
    def delete_question(qid):
        '''removes the question with the provided id from the database'''
        question = Question.by_id(int(qid))
        if g.lti.is_instructor():
            session.delete(question)
            session.commit()

        return json.dumps({'deleted': g.lti.is_instructor()})

    @staticmethod
    def ask_question(instructor):
        '''passes the name of the course instructor to the ask question module and calls the screen to ask a question'''
        return render_template('askQuestion.html', instr=instructor)

    @staticmethod
    def create_question(question, instructor, course, active, time, comment, tags, rating):
        '''formats a question for database insertion and inserts it, calls a result screen afterwards'''
        try:
            time = int(time)
        except ValueError:
            time = 0
        session.add(Question(instructor, course, question, active, time, comment, tags, rating))
        session.commit()
        return QuestionController.get_list_asked()

    @staticmethod
    def calculate_remaining_time(question):
        time_remaining = datetime.now() - (question.activate_time +
                timedelta(seconds=question.time))
        time_remaining = time_remaining.seconds + time_remaining.days * 86400
        return - time_remaining
