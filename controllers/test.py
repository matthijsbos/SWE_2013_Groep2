from google.appengine.ext import webapp
from imslti.ltilaunch import LTI_Launch
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
            launchdict = { 
                'isinstructor' : launch.isInstructor(),
                'consumerkey' : launch.getConsumerKey(),
                'coursekey' : launch.getCourseKey(),
                'coursename': launch.getCourseName(),
            
                         }


            params = urllib.urlencode(launchdict)

            conn.request("POST", self.request.path, params)
            self.response.out.write(conn.getresponse().read())
