from flask import render_template, g
from models.Index import ModelIndex

class Index():
    def __init__(self,request):
        self.request = request

    def render(self):
        return render_template('index.html', lti_dump=g.lti.dump_all())
