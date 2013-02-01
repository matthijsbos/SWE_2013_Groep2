from models.user import UserModel
from utilities import render_template

class User():
    def __init__(self, request):
        self.request = request
        
    def __repr__(self):
        return "<User ('%s', '%s', '%s')>" % (self.userid, self.username, self.trust)
        
    def render_with_all(self):
        return render_template('trustdata_start.html', data=UserModel.get_all())

    def render_by_username(self, uid):
        return render_template('trustdata_start.html', data=UserModel.get_by_username(uid))
        
