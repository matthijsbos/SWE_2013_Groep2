# Authors : Victor Azizi & David Schoorisse & Mustafa Karaalioglu
# Descrp : Controls the creation and deletion of tags
# Changes:
# Comment:

from flask import session as fsession, g
from utilities import render_template
from models.tag import Tag, AnswerTag
from models.answer import AnswerModel
import json


class Modifytags():
    def __init__(self):
        pass
    
    def addtag(self, args):
        tag = args['tag']
        if tag != '':
            response = Tag.add_tag(tag);
            if not response:                
                return json.dumps({"succes": False})
            else:
                return json.dumps({"succes": True, "id":response})
        else:
            return json.dumps({"succes": False})

    def delete_tag_question(self, id):
        if g.lti.is_instructor():
            Tag.remove_tag(id)
        return json.dumps({'deleted': g.lti.is_instructor()})

    def render(self):
        self.taglist = Tag.get_all()
        return render_template('modifytags.html',tags=self.taglist)        
        
    @staticmethod
    def json_get_tags(q):    
       tags = Tag.get_searched_tags(q)
       data = []
       for tag in tags:
           data.append( {"id":str(tag.id), "name":tag.name} )
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
