# Author : Victor Azizi
# Descrp : Controls the creation and deletion of tags
# Changes:
# Comment:

from flask import render_template
from models.tag import Tag
from dbconnection import session


class Modifytags():
    def __init__(self):
        pass

    def addtag(self, request):
        Tag.add_tag(request.form['newTag'])

    def deletetag(self, request):
        for tid in request.form.getlist('tags'):
            Tag.remove_tag(tid)

    def render(self):
        self.taglist = []
        for tag in session.query(Tag):
            self.taglist.append(tag)

        return render_template('modifytags.html', tags=self.taglist)
