# Author : Victor Azizi
# Descrp : Controls the creation and deletion of tags
# Changes:
# Comment:

from flask import render_template
from models.tags import Tag
from dbconnection import session

class ModifyTags():
    def __init__(self):
        taglist = []
        for tag in session.query(Tag):
            taglist.append(tag)

    def render(self):
        return render_template('modifyTags.html',tags=taglist)
