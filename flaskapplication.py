# Author : Dexter Drupsteen
# Descrp : Contains routing and calling of the constrollers
# Changes: 
# Comment: MultiDict with isinstructor,consumerkey,coursekey and coursename in
#          the request.form field.

from flask import Flask,request,render_template
from controllers import hello

app = Flask(__name__)

@app.route("/",methods=['POST'])
def home():
    return "fuck me"

@app.route("/test",methods=['POST'])
def test():
    return "You posted it didn't you?"

@app.route("/launch",methods=['POST'])
def launch():
    ctrler = hello.Hello()
    return ctrler.render()

if __name__ == '__main__':
        app.run()
        
