from models import answer, question, user
from models.question import Question
from models.answer import AnswerModel
from models.tag import AnswerTag, Tag
from flask import g, request, redirect
from utilities import render_template
from dbconnection import session
import datetime
import time
import json
import sqlalchemy.orm.exc as sqlalchemyExp


class Answer():
    def render(self):
        # dummy shit, get some real data
        qText = 'wat is het antwoord op deze dummy vraag?'
        questionStartTime = datetime.datetime.now();
        uID = g.lti.get_user_id()
        qID = -1
        timerD = 25        

        # Post should be real data
        if request.method == 'POST' and 'questionID' in request.form:
            qID = int(request.form['questionID'])
            q = question.Question.by_id(qID)
            if q is not None:
                qText = q.question
                questionStartTime = q.activate_time;
                timerD = q.time

        print 'Retrieved question information'
        if 'answerText' in request.values:
            answerText = request.form['answerText']
            print self.saveAnswer(uID, qID, timerD, questionStartTime,
                    answerText)
            return json.dumps({"result":True})
        elif 'showall' in request.values:
            # Render all
            return self.render_all()
        elif 'viewanswer' in request.values:
            # show answer
            return self.viewAnswer()
        elif 'reviewAnswer' in request.values:
            # save review answer
            return self.saveReviewAnswer()
        elif 'removeAnswer' in request.values:
            return self.removeAnswer()
        else:
            return self.answerQuestion(uID, qID, qText, timerD,
                    questionStartTime)

    @staticmethod
    def renderanswerform():
        try:
            questionid = int(request.values['question_id'])
            question = Question.by_id(questionid)
        except:
            return abort(404)
        return render_template('student_answer.html', question = question)

    @staticmethod
    def save():
        try:
            questionid = int(request.values['questionid'])
            question = Question.by_id(questionid)
            text = request.values['text']
            userid = g.lti.get_user_id()
        except:
            return abort(404)

        if AnswerModel.question_valid(questionid) and text != "":
            AnswerModel.save(questionid, userid, text)

        return redirect('/index_student')

    def saveAnswer(self, uID, qID, timerD, questionStartTime, answerText):
        # save answer
        #print "ANSW", uID, qID, timerD
        #answerText = request.form['answerText']

        flag = "false"
        if self.timeLeft(timerD, questionStartTime):
            if answer.AnswerModel.check_answer_exists(uID, qID):
                aID = answer.AnswerModel.get_answer_id(uID, qID)
                answer.AnswerModel.update_answer(aID, answerText)
            else:
                answer.AnswerModel.save(qID, uID, answerText)
            flag = "true"
        return True#render_template('answersaved.html', flag=flag)

    def viewAnswer(self):
        aid = int(request.form['id'])
        return render_template('editanswer.html', answer=AnswerModel.by_id(aid))

    def saveReviewAnswer(self):
        questionID = int(request.form['questionID'])
        userID = request.form['userID']
        reviewAnswer = request.form['reviewAnswer']
        edit = int(request.form['edit'])
        answer.AnswerModel.savereview(
            questionID, userID, reviewAnswer, edit)
        return render_template('answersaved.html', flag='true')

    def removeAnswer(self):
        id = int(request.form['id'])
        answer.AnswerModel.remove_by_id(id)
        return render_template('answersaved.html', flag='removed')

    def answerQuestion(self, uID, qID, qText, timerD, questionStartTime):
        go = "true"
        if answer.AnswerModel.check_answer_exists(uID, qID):
            aID = answer.AnswerModel.get_answer_id(uID, qID)
            if not self.timeLeft(timerD, questionStartTime):
                go = "false"
        return render_template('answer.html',
                                questionID=qID,
                                userID=uID,
                                questionText=qText,
                                timerDuration=timerD,
                                date=time.mktime(questionStartTime.timetuple()),
                                go=go)

    def timeLeft(self, timerD, questionStartTime):
        currentTime = datetime.datetime.now()
        timeAnswered = questionStartTime
        difference = currentTime - timeAnswered
        seconds = difference.days * 86400 + difference.seconds

        if timerD == 0:
            return True
        else:
            if seconds < timerD + 20:
                return True
            else:
                return False

    def render_results(self):
        qid = request.values["questionid"]
        answers = AnswerModel.get_answers_ordered_by_rank(qid)
        return render_template('rankresults.html', answers=answers)

    def render_all(self):
        # Render all
        return render_template('showanswers.html',
                answers=answer.AnswerModel.get_all())

    def render_filtered(self,questionID=None,data=None):        
        return render_template('answerfilter.html',
                hasqid=(questionID is not None),
                questionID=questionID, data_set=data)

    def render_filtered_tbl(self,limit,offset,**kwargs):
        (answers, curpage, maxpages, startpage, pagecount) = \
                self.get_filtered(limit=limit, offset=offset)

        hasqid = ('questionID'in kwargs)
        course = g.lti.get_course_id()
        
        for a in answers:
            a.tags = ''
            tag_ids = AnswerTag.get_tag_ids(a.id)
            if tag_ids != []:           
                for id in tag_ids:
                    tag_name = Tag.get_tag(id)                     
                    a.tags += tag_name + ', ' 
                a.tags = a.tags[:-2]            

        return render_template('answer_filter_tbl.html',
                answers=answers,currentpage=curpage,
                maxpages=maxpages,startpage=startpage,pagecount=pagecount,
                hasQuestionID=hasqid,
                users=user.UserModel.get_all(),
                questions = [] if hasqid else Question.by_course_id(course))

    def get_filtered(self,limit=None,offset=None):
        args = self.get_args_for_filter()

        if len(args) > 0:
            if offset is None or limit is None:
                return answer.AnswerModel.get_filtered(**args)
            else:
                return answer.AnswerModel.get_filtered_offset(limit,
                                                              offset,
                                                              orderby='created',
                                                              **args)
        else:
            if offset is None or limit is None:
                return AnswerModel.get_filtered()
            else:
                return AnswerModel.get_filtered_offset(limit,
                                                       offset,
                                                       orderby='created')

    def get_args_for_filter(self):
        postdata = request.form if request.method == 'POST' else request.args

        args = {}
        if "questionID" in postdata and len(postdata["questionID"]) > 0:
            args["questionID"] = postdata["questionID"]
        if "userID" in postdata and len(postdata["userID"]) > 0:
            args["userID"] = postdata["userID"]
        if "id" in postdata and len(postdata["id"]) > 0:
            args["id"] = postdata["id"]

        return args

    def studenthistory(self):
        return render_template('studenthistory.html')

    def studenthistory_result(self):
        return render_template('studenthistory_result.html',
                studid=AnswerModel.get_answers_by_userid(request.values['sid']))

