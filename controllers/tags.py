# Authors : Victor Azizi & David Schoorisse & Mustafa Karaalioglu
# Descrp : Controls the creation and deletion of tags
# Changes:
# Comment:

from flask import render_template
from models.tags import Tag, AnswerTag
from models.answer import AnswerModel
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

        return render_template('modifytags.html',tags=self.taglist)


class AssignTags():
    def __init__(self, answer_id):
        self.answer_id = answer_id
    
    def assign(self, tag_id):
        if self.answer is not None:
            answer_tag = AnswerTag(self.answer_id, tag_id)
            
            if session.query(AnswerTag).filter(
                AnswerTag.answer_id==self.answer_id,
                AnswerTag.tag_id==tag_id).first() is None:
                    session.add(answer_tag)
    
    def render(self):
        return render_template('showanswers.html', answers=AnswerTag.get_all(),
                               tags=Tags.get_all())