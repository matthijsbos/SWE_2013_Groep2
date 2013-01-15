# Author : Dexter Drupsteen
# Descrp : Contains routing and calling of the constrollers
# Changes: 
# Comment: MultiDict with isinstructor,consumerkey,coursekey and coursename in
#          the request.form field.

from flask import Flask,request,render_template
from controllers import hello, modifytags

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
    ctrler = hello.Hello()
    return ctrler.render()

@app.route("/managetags",methods=['GET'])
def managetags():
    ctrler = modifytags.ModifyTags()
    return ctrler.render()

@app.route("/addtag",methods=['POST'])
def addtags():
    ctrler = modifytags.AddTag(request)
    return ctrler.render()

if __name__ == '__main__':
    app.run()
        
