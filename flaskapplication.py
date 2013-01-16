# Author : Dexter Drupsteen
# Descrp : Contains routing and calling of the controllers
# Changes:
# Comment:

import yaml
from flask import Flask, Response, request, render_template, g

from lti import LTI, LTIException
from controllers.index import Index
from controllers.answer import Answer
from controllers.question import QuestionController as Question

app = Flask(__name__)
app.debug = True
app.secret_key = "Hurdygurdy" # Used for Flask sessions, TODO: config?

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
@app.route("/",methods=['GET', 'POST'])
def home():
    ctrler = Index(request)
    return ctrler.render()

@app.route("/launch",methods=['POST'])
def launch():
    ctrler = Index(request)
    return ctrler.render()

# this route is used to ask a question to students
@app.route("/question",methods=['GET', 'POST'])
def ask_question():
    if g.lti.is_instructor() == False:
        return render_template("access_restricted.html")

    return Question.ask_question(g.lti.get_user_id())

# this route is used for the feedback from inserting the question into the
# database, it also inserts the question into the database
@app.route("/handle_question",methods=['POST'])
def handle_question():
    if g.lti.is_instructor() == False:
      return render_template("access_restricted.html")
    return Question.create_question(request.form['question'],
            g.lti.get_user_id(),g.lti.get_course_id(),request.form['time'])

@app.route("/question_list", methods=['GET', 'POST'])
def list_questions():
    return Question.get_list()

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


@app.route("/answer",methods=['GET', 'POST'])
def answerForm():
    ctrler = Answer(request)
    return ctrler.render()

@app.route("/logout")
def logout():
    g.lti.destroy()
    return "Logged out..."

if __name__ == '__main__':
        app.run()

