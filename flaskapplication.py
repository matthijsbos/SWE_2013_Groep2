# Author : Dexter Drupsteen
# Descrp : Contains routing and calling of the constrollers
# Changes: 
# Comment: MultiDict with isinstructor,consumerkey,coursekey and coursename in
#          the request.form field.

from flask import Flask, request, render_template, g
from lti import LTI, LTIException
from controllers import index, answer, modifytags

app = Flask(__name__)
app.debug = True
app.secret_key = "Hurdygurdy"

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
    ctrler = index.Index(request)
    return ctrler.render()

@app.route("/test",methods=['POST'])
def test():
    return "You posted it didn't you?"

@app.route("/launch",methods=['POST'])
def launch():
    ctrler = index.Index(request)
    return ctrler.render()

@app.route("/managetags",methods=['POST'])
def managetags():
    ctrler = modifytags.Modifytags()
    return ctrler.render()

@app.route("/addtag",methods=['POST'])
def addtags():
    ctrler = modifytags.Modifytags()
    ctrler.addtag(request)
    return ctrler.render()

@app.route("/removetag",methods=['POST'])
def removetags():
    ctrler = modifytags.Modifytags()
    ctrler.deletetag(request)
    return ctrler.render()
    

@app.route("/answer",methods=['POST','GET'])
def answerForm():
    ctrler = answer.Answer(request)
    return ctrler.render()

@app.route("/filteranswers",methods=['POST','GET'])
def answerForm():
    ctrler = answer.Answer(request)
    return ctrler.render_filtered()

@app.route("/logout")
def logout():
    g.lti.destroy()
    return "Logged out..."

if __name__ == '__main__':
        app.run()
        
