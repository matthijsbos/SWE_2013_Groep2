# Authors : Victor Azizi & David Schoorisse & Mustafa Karaalioglu
# Descrp : Controls the creation and deletion of tags
# Changes:
# Comment:

<<<<<<< HEAD
from flask import render_template, session as fsession, g
=======
from flask import session as fsession
from utilities import render_template
>>>>>>> dd1922c6702b5871889539e90c615129addb9562
from models.tag import Tag, AnswerTag
from models.answer import AnswerModel
import json


class Modifytags():
    def __init__(self):
        pass
    
    def addtag(self, request):
        Tag.add_tag(request.form['newTag'])

<<<<<<< HEAD
    def delete_tag_question(self, id):
        if g.lti.is_instructor():
            Tag.remove_tag_question(id)
        return json.dumps({'deleted': g.lti.is_instructor()})
=======
    def deletetag(self, request):
        for tid in request.form.getlist('tags'):
            Tag.remove_tag(tid)
>>>>>>> dd1922c6702b5871889539e90c615129addb9562

    def render(self):
        self.taglist = Tag.get_all()
        return render_template('modifytags.html',tags=self.taglist)
        
    @staticmethod
    def json_get_tags():    
       #create json file of all tags
       data = Tag.get_all()

       #list of dicytionaries
       data = [
                   {"id":"856","name":"Ruby"},
                   {"id":"1035","name":"Python"},
                   {"id":"856","name":"JavaScript"},
                   {"id":"1035","name":"ActionScript"},
                   {"id":"856","name":"Scheme"},
                   {"id":"1035","name":"Lisp"},
                   {"id":"1035","name":"Visual Basic"},
                   {"id":"856","name":"C"},
                   {"id":"856","name":"Java"}
       ]

       #Qreturn "Test return"
       return json.dumps(data)


class AssignTags():
    def __init__(self, answer_id):
        self.answer_id = answer_id
        self.answer = AnswerModel.by_id(answer_id)
        if self.answer == None:
            self.answer = "Error, Answer not found"

        fsession['assigntag'] = str(answer_id)
    
    @staticmethod
    def assign(request):
        for tag_id in request.form.getlist('tags'):
            AnswerTag.add_answertag(fsession['assigntag'], tag_id)
            
    @staticmethod
    def remove(request):
        for tag_id in request.form.getlist('tags'):
            AnswerTag.remove(fsession['assigntag'], tag_id)
              
    def render(self):
        enabledtags = AnswerTag.get_tag_ids(self.answer_id)
        return render_template('assigntag.html', answer=self.answer,
                               tags=Tag.get_all(), enabledtags=enabledtags)
