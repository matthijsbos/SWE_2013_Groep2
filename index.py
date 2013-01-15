import os
import wsgiref.handlers
from google.appengine.ext import webapp
from imslti.ltilaunch import LTI_Launch
import httplib
import urllib

class LaunchHandler(webapp.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        # Loads the LTI data/session
        launch = LTI_Launch(self)
        if launch.complete:
            return

        if launch.loaded:
            conn = httplib.HTTPConnection('localhost', 5000)   

            # Dont include launch object yet, keep it simple for now ...
            # Shouldn't be too much work though
            launchdict = { 
                'isinstructor' : launch.isInstructor(),
                'userkey' : launch.getUserKey(),
                'resourcekey' : launch.getResourceKey(),
                'consumerkey' : launch.getConsumerKey(),
                'coursekey' : launch.getCourseKey(),
                'coursename': launch.getCourseName(),
            
                         }
            
            for argument in self.request.arguments():
                launchdict[argument] = self.request.get(argument)

            params = urllib.urlencode(launchdict)

            conn.request("POST", self.request.path, params)
            self.response.out.write(conn.getresponse().read())

        else:
            self.response.out.write('<p>This tool must be launched using ' +
                    'IMS Basic LTI.</p>')


        self.response.out.write('\n'+launch.dump()+'\n');


class IndexHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""<a href="/launch">Launch</a>""")

def main():
    # Add routes (ie. uri's which are bound to a class to handle that location)
    routes = [ ('/launch', LaunchHandler) ]
    routes.append( ('/.*', IndexHandler) )

    application = webapp.WSGIApplication(routes, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
