# Author : Dexter Drupsteen
# Descrp : Contains controller logic for the hello mvc
# Changes:
# Comment:

from flask import render_template
from models.Hello import Model

class Hello():
    def __init__(self):
        pass

    def render(self):
        return render_template('hello.html',wordlist=Model.getall())
