# Author : Dexter Drupsteen
# Descrp : Contains controller logic for the hello mvc
# Changes:
# Comment:

from flask import render_template
from models.Hello import Model
from dbconnection import session

class Hello():
    def __init__(self):
        # create a few database items
        for model in session.query(Model):
            break
        else:
            session.add(Model("hello"))
            session.add(Model("Groep"))
            session.add(Model("2"))
            session.commit()


    def render(self):
        return render_template('hello.html',wordlist=Model.getall())
