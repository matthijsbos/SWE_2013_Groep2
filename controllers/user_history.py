from models.user_history import UserHistoryModel
from models.user import UserModel
from utilities import render_template

class UserHistory():
    def __init__(self, request):
        self.request = request
        
    def __repr__(self):
        return "<UserHistory ('%s', '%s', '%s', '%s')>" % (self.key, self.userid, self.time, self.trust)

    def render_by_userid(self, uid):
        return render_template('trustdata.html', data=UserHistoryModel.get_by_user_id(uid), data2=UserModel.by_user_id(uid))
        