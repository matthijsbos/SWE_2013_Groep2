import os
import wsgiref.handlers
from google.appengine.ext import webapp
from imslti.ltilaunch import LTI_Launch
from controllers.test import Test

class LaunchHandler(webapp.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        # Loads the LTI data/session
        launch = LTI_Launch(self)
        if launch.complete:
            return

        if launch.loaded:
            self.response.out.write('<a href="' +
                    launch.getUrl() +
                    '" target="_new">Open (with session)</a></p>')

            # Value is preserved in this session
            val = launch.get('val', 0)
            self.response.out.write('<p>Val '+str(val)+'</p>')
            launch['val'] = val + 1
        else:
            self.response.out.write('<p>This tool must be launched using ' +
                    'IMS Basic LTI.</p>')


        self.response.out.write('\n'+launch.dump()+'\n');


class IndexHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""<a href="/launch">Launch</a>""")

def main():
    # Add routes (ie. uri's which are bound to a class to handle that location)

    routes = [ ('/launch', Test) ]
    routes.append( ('/test', Test) ) 
    routes.append( ('/.*', IndexHandler) )

    application = webapp.WSGIApplication(routes, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
