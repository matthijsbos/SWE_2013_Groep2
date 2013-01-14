from google.appengine.ext import webapp
from imslti.ltilaunch import LTI_Launch
import pickle
import marshal
import httplib
import urllib

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
            seriallaunch = pickle.dumps(launch, -1)
            #seriallaunch = marshal.dumps(launch, -1)
            params = urllib.urlencode({ 'launch':seriallaunch})

            conn.request("POST", self.request.path, params)
            self.response.out.write(conn.getresponse().read())
