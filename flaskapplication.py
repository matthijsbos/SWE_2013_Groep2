# Author : Dexter Drupsteen
# Descrp : Contains routing and calling of the constrollers
# Changes: 
# Comment: MultiDict with isinstructor,consumerkey,coursekey and coursename in
#          the request.form field.

from flask import Flask,request,render_template
from controllers import index, answer

app = Flask(__name__)
app.debug = True

# define the routes for our application
@app.route("/",methods=['POST'])
def home():
    return "This is not the way to call the application"

@app.route("/test",methods=['POST'])
def test():
    return "You posted it didn't you?"

@app.route("/launch",methods=['POST'])
def launch():
    ctrler = index.Index(request)
    return ctrler.render()

@app.route("/answer",methods=['POST'])
def answerForm():
    ctrler = answer.Answer(request)
    return ctrler.render()

if __name__ == '__main__':
        app.run()
        
