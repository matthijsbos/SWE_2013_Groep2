from google.appengine.ext import webapp
from imslti.ltilaunch import LTI_Launch
import json
import httplib

class Test(webapp.RequestHandler):
    def get(self):
        self.post()
    def post(self):
        # Loads the LTI data/session
        launch = LTI_Launch(self)

        if launch.loaded:
            conn = httplib.HTTPConnection('localhost', 5000)

            # Dont include launch object yet, keep it simple for now ...
            # Shouldn't be too much work though
            conn.request("POST", self.request.path)
            self.response.out.write(conn.getresponse().read())
