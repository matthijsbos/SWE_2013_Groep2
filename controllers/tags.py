# Authors : Victor Azizi & David Schoorisse & Mustafa Karaalioglu
# Descrp : Controls the creation and deletion of tags
# Changes:
# Comment:

from flask import render_template, session as fsession
from models.tag import Tag, AnswerTag
from models.answer import AnswerModel
from dbconnection import session
import json

#create json file of all tags
data = Tag.get_all()
tags = json.dumps(data)

class Modifytags():
    def __init__(self):
        pass
    
    def addtag(self, request):
        Tag.add_tag(request.form['newTag'])

    def deletetag(self, request):
        for tid in request.form.getlist('tags'):
            Tag.remove_tag(tid)

    def render(self):
        self.taglist = Tag.get_all()
        return render_template('modifytags.html',tags=self.taglist)


class AssignTags():
    def __init__(self, answer_id):
        self.answer_id = answer_id
        try:
            self.answer = AnswerModel.by_id(answer_id)
        except:
            self.answer = "Error, Answer not found"
        fsession['assigntag'] = str(answer_id)
    
    @staticmethod
    def assign(request):
        for tag_id in request.form.getlist('tags'):
            AnswerTag.add_answertag(fsession['assigntag'], tag_id)
              
    def render(self):
        enabledtags = AnswerTag.get_tag_ids(self.answer_id)
        return render_template('assigntag.html', answer=self.answer,
                               tags=Tag.get_all(), enabledtags=enabledtags)
