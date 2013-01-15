# Author : Victor Azizi
# Descrp : Controls the creation and deletion of tags
# Changes:
# Comment:

from flask import render_template
from models.tags import Tag
from dbconnection import session

class ModifyTags():
    def __init__(self):
        self.taglist = []
        for tag in session.query(Tag):
            self.taglist.append(tag)

    def render(self):
        return render_template('modifyTags.html',tags=self.taglist)

class AddTag():
    def __init__(self, request):
        for tag in session.query(Tag):
            if tag.name == request.form['newTag']:
                break
        else:
            session.add(Tag(request.form['newTag']))
            session.commit()


        self.taglist = []
        for tag in session.query(Tag):
            self.taglist.append(tag)

    def render(self):
        return render_template('modifyTags.html',tags=self.taglist)
