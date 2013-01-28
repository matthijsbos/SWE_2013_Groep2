# Descrp : Contains routing and calling of the constrollers
# Changes:
# Comment: MultiDict with isinstructor,consumerkey,coursekey and coursename in
#          the request.form field.

import models.question
import models.answer
import models.answerchoice
import models.tag
import models.rating
from dbconnection import Base, engine
from flask import Flask, request, render_template, g
from lti import LTI, LTIException
from controllers import index, answer, answerchoice
import yaml
import json
from flask import Flask, Response, request, g
from utilities import render_template
from lti import LTI, LTIException
from controllers.index import Index
from controllers.answer import Answer
from controllers.question import QuestionController as Question
from controllers.tags import Modifytags, AssignTags
from controllers.review import ReviewAnswer

app = Flask(__name__)
app.debug = True
app.secret_key = "Hurdygurdy"  # Used for Flask sessions, TODO: config?


@app.before_request
def init_lti():
    """Starts (or resumes) the LTI session before anything else is handled.

    When no LTI session is available, an error page will be displayed."""

    params = {}
    if request.method == 'POST':
        params = request.form.to_dict()
    else:
        params = request.args.to_dict()

    try:
        g.lti = LTI(request.url, params, dict(request.headers))
    except LTIException as error:
        ret = "Error getting LTI data. Did you run this tool via a " + \
            "consumer such as Sakai?"
        if app.debug:
            ret += "<hr>Debug info:<br/>%s" % str(error)
        return ret


# define the routes for our application
@app.route("/", methods=['GET', 'POST'])
def home():
    ctrler = Index()
    return ctrler.render()


@app.route("/debug", methods=['GET', 'POST'])
def launch():
    ctrler = Index(debug=True)
    return ctrler.render()


@app.route("/edit_question", methods=['GET', 'POST'])
def edit_question():
    return Question.edit_question(request.args['id'],
                                  request.args['text'],
                                  request.args['time'])

# this route is called to toggle a question's availability


@app.route("/toggle_question", methods=['GET', 'POST'])
def toggle_question():
    return Question.toggle_question(request.args['id'], request.args['field'])

@app.route("/questionavailability", methods=['GET', 'POST'])
def questionavailability():
    return Question.availability(request.args)

# this route is used to ask a question to students


@app.route("/question", methods=['GET', 'POST'])
def ask_question():
    if g.lti.is_instructor() == False:
        return render_template("access_restricted.html")

    return Question.ask_question(g.lti.get_user_id())

# this route is used for the feedback from inserting the question into the
# database, it also inserts the question into the database


@app.route("/handle_question", methods=['POST'])
def handle_question():
    try:
        isActive = request.form['active'] in ['true','True']
    except:
        isActive = False

    try:
        comment = request.form['comment'] in ['true','True'] 
    except:
        comment = False

    try:
        tags = request.form['tags'] in ['true','True']
    except:
        tags = False

    try:
        rating = request.form['rating'] in ['true','True']
    except:
        rating = False

    Question.create_question(request.form['question'],
                                    g.lti.get_user_id(),
                                    g.lti.get_course_id(),
                                    isActive,
                                    request.form['time'],
                                    comment,
                                    tags,
                                    rating)
    return json.dumps({'done':True})


@app.route("/question_list", methods=['GET', 'POST'])                                            
def list_questions():
    return render_template('question_list.html')

@app.route("/question_list_table",methods=['GET','POST'])
def list_questions_table():
    limit = 20
    offset = 0

    if 'limit' in request.args:
        limit = int(request.args['limit'])
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    return Question.get_list_table(limit,offset)

@app.route("/question_list/asked", methods=['GET', 'POST'])
def list_questions_asked():
    return Question.get_list_asked()

@app.route("/question_list/to_answer", methods=['GET', 'POST'])
def list_questions_answer():
    return Question.get_list_to_answer()

@app.route("/delete_question/<id>", methods=['GET', 'POST'])
def delete_question(id):
    return Question.delete_question(id)


@app.route("/question_export", methods=['GET', 'POST'])
def question_export():
    exp = Question.export_course(g.lti.get_course_id())
    exp = yaml.dump(exp, default_flow_style=False)
    return Response(exp,
                    mimetype="text/plain",
                    headers={"Content-Disposition":
                             "attachment;filename=questions_%s.yaml" %
                    g.lti.get_course_name()})

@app.route("/question_import", methods=['GET', 'POST'])
def question_import():
    list = yaml.load(request.args['file'])
    print list

@app.route("/managetags", methods=['GET', 'POST'])
def managetags():
    ctrler = Modifytags()
    return ctrler.render()


@app.route("/addtag", methods=['POST'])
def addtags():
    ctrler = Modifytags()
    ctrler.addtag(request)
    return ctrler.render()


@app.route("/removetag", methods=['GET'])
def removetags():
    ctrler = Modifytags()
    return ctrler.delete_tag_question(request.args['tagid'])
    #return ctrler.render()


@app.route("/removetaganswer", methods=['POST', 'GET'])
def removetag_answer():
    ctrler = ReviewAnswer(request)
    return ctrler.remove_tag_answer(request.args['answerid'], request.args['tagid'])


@app.route("/addtaganswer", methods=['POST', 'GET'])
def addtag_answer():
    ctrler = ReviewAnswer(request)
    return ctrler.add_tag_answer(request.args['answerid'], request.args['tagid'])


@app.route("/answer", methods=['GET', 'POST'])
def answerForm():
    ctrler = Answer(request)
    return ctrler.render()

@app.route("/answerchoice",methods=['GET'])
def answerChoice():
    ctrler = answerchoice.Answerchoice(request)
    return ctrler.render()

@app.route("/answerchoice",methods=['POST'])
def processanswerchoice():
    ctrler = answerchoice.Answerchoice(request)
    return ctrler.process()

@app.route("/choicelobby",methods=['GET'])
def lobby():
    ctrler = answerchoice.Answerchoice(request)
    return ctrler.lobby()

@app.route("/assigntags", methods=['POST', 'GET'])
def assign_tags():
    ctrler = AssignTags(1)
    return ctrler.render()


@app.route("/assigntags_done", methods=['POST'])
def handle_assign_tags():
    ctrler = AssignTags.assign(request)
    return "<a href='/'>back to main</a>"

@app.route("/removetags_done",methods=['POST'])
def handle_remove_tags():
    ctrler = AssignTags.remove(request)
    return Index(request).render()

@app.route("/json/get_tags",methods=['POST', 'GET'])
def json_get_tags():
    return Modifytags.json_get_tags()

"""
To review a answer, return reviewanswer.review(x) should be called from the
controller deciding wich answer to review, this url handles storing the reviews
in the database (given a user has permission to do so)
"""
@app.route("/reviewanswer",methods=['POST', 'GET'])
def handle_review_answer():
    ctrler = ReviewAnswer(request)
    return ReviewAnswer.review()

@app.route("/reviewanswer_stub", methods=["POST", "GET"])
def do_review_answer_stub():
    return ReviewAnswer.review()

@app.route("/filteranswers", methods=['POST', 'GET'])
def answerFilter():
    ctrler = Answer(request)
    return ctrler.render_filtered()

@app.route("/rankresults", methods=['POST', 'GET'])
def render_results():
    ctrler = answer.Answer(request)
    return ctrler.render_results()


@app.route("/filteranswers/<questionid>", methods=['POST', 'GET'])
def answerFilterByQuestionID(questionid):
    ctrler = Answer(request)
    return ctrler.render_filtered_by_questionid(questionid)


@app.route("/has_new_question", methods=['GET', 'POST'])
def has_new_question():
    ctrler = Index()
    return ctrler.has_new_question()

@app.route("/answerit", methods=['GET'])
def answer_it_GET():
    return Answer.renderanswerform()

@app.route("/answerit", methods=['POST'])
def answer_it_POST():
    return Answer.save()

@app.route("/has_new_review", methods=['GET', 'POST'])
def has_new_review():
    return ReviewAnswer.has_new_review()

@app.route("/question_remaining_time",methods=['GET','POST'])
def get_question_remaining_time():
    return Question().get_remaining_time(request.args['questionID'])

@app.route("/pagination",methods=['GET'])
def get_pagination():
    curpage = int(request.args['currentpage'])
    startpage = int(request.args['startpage'])
    pagecount =  int(request.args['pagecount'])
    maxpages = int(request.args['maxpages'])

    return render_template('pagination.html',currentpage=curpage,
            startpage=startpage,pagecount=pagecount,maxpages=maxpages)

@app.route("/logout")
def logout():
    g.lti.destroy()
    return "Logged out..."

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0')
