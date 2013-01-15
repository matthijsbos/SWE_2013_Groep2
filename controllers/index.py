from flask import render_template
from models.Index import ModelIndex

class Index():
    def __init__(self,request):
        self.request = request


    def render(self):
        return render_template('index.html')
