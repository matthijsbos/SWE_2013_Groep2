# Author : Dexter Drupsteen
# Descrp : Contains routing and calling of the constrollers
# Changes:
# Comment: MultiDict with isinstructor,consumerkey,coursekey and coursename in
#          the request.form field.

from flask import Flask, request, render_template, g
from lti import LTI, LTIException
from controllers import hello

app = Flask(__name__)
app.debug = True
app.secret_key = "Hurdygurdy"

@app.before_request
def init_lti():
    params = {}
    if request.method == 'POST':
        params = request.form.to_dict()
    else:
        params =request.args.to_dict()

    try:
        g.lti = LTI(request.url, params, dict(request.headers))
    except LTIException as error:
        ret = "Error getting LTI data. Did you run this tool via a " + \
                "consumer such as Sakai?"
        if app.debug:
            ret += "<hr>Debug info:<br/>%s" % str(error)
        return ret

    else:
        print g.lti.dump_all()

# define the routes for our application
@app.route("/",methods=['GET', 'POST'])
def home():
    return "This is not the way to call the application"

@app.route("/test",methods=['POST'])
def test():
    return "You posted it didn't you?"

@app.route("/launch",methods=['POST'])
def launch():
    ctrler = hello.Hello()
    return ctrler.render()

@app.route("/logout")
def logout():
    g.lti.destroy()
    return "Logged out..."

if __name__ == '__main__':
        app.run()

