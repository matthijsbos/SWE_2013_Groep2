import json
from flask import escape, g
from utilities import render_template
from dbconnection import session
from models.question import Question
from datetime import datetime, timedelta

from controllers.scheduler import Scheduler


class QuestionController():
    # TODO: remove toggle_question, fix availability
    @staticmethod
    def toggle_options(args):
            try:
                type = args['type']
            except KeyError:
                return

            question = Question.by_id(args['id'])
            if question is None:
                return

            if not g.lti.is_instructor() and type != 'Reviewable':
                return

            rv = None
            if type == 'Inactive':
                rv = question.inactive = True
                question.answerable = question.reviewable = question.archived = False
                question.state = 'Inactive'

            if type == 'Answerable':
                rv = question.answerable = True
                question.activate_time = datetime.now()
                question.inactive = question.reviewable = question.archived = False
                question.state = 'Answerable'

            elif type == 'Reviewable':
                if not question.reviewable:
                    Scheduler(args['id'])
                    question.reviewable = True
                rv = question.reviewable
                question.inactive = question.answerable = question.archived = False
                question.state = 'Reviewable'

            elif type == 'Archived':
                rv = question.archived = True
                question.inactive = question.answerable = question.reviewable = False
                question.state = 'Archived'

            elif type == 'comments':
                rv = question.comment = not question.comment

            elif type == 'tags':
                rv = question.tags = not question.tags

            elif type == 'rating':
                rv = question.rating = not question.rating

            session.commit()
            return json.dumps({"toggle": rv, "check": True})

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
            activate = q.answerable

            session.add(q)
            session.commit()

            return json.dumps({"id": q_id,
                               "text": escaped_question,
                               "answerable": activate,
                               "time":time,
                               "check": g.lti.is_instructor()})
        else:
            return json.dumps({"id": q_id,
                               "text": question,
                               "answerable": activate,
                               "time": time,
                               "check": g.lti.is_instructor()})

    @staticmethod
    def get_remaining_time(q_id):
        question = Question.by_id(q_id)

        if question is not None and question.activate_time is not None:
            time_remaining = question.get_time_left()
            question_time =  question.time
        else:
            time_remaining = 0
            question_time =  0

        return json.dumps({"still_answerable":((question is not None) and question.answerable),
                           "time_remaining":time_remaining,
                           "question_deleted":(question is None) or not question.answerable,
                           "question_time":question_time})

    @staticmethod
    def get_questions(n):
        """Retrieves the first n questions, sorted by date answerable."""
        return session.query(Question).order_by(Question.answerable.desc())[:n]

    @staticmethod
    def export_course(course_id):
        questions = Question.by_course_id(course_id)
        return [{'question': question.question} for question in questions]

    @staticmethod
    def import_course(user_id, course_id, data):
        for question in data:
            QuestionController.create_question(question['question'], user_id,
                    course_id, False, 0, True, True, True)

        questions = map(lambda x: x['question'], data)
        return render_template('import.html', questions=questions)

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
                if question.get_time_left() < 0:
                    question.answerable = False
        session.commit()
        return render_template('question_list.html', questions=questions)

    @staticmethod
    def get_list_table(limit,offset):
        (questions, curpage, maxpages, startpage, pagecount) = Question.get_filtered_offset(limit,offset,orderby='created')

        for question in questions:
            if question is not None and question.activate_time is not None:
                if question.get_time_left() < 0:
                    question.answerable = False
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
