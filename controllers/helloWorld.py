import jinja2
from google.appengine.ext import webapp
from imslti.ltilaunch import LTI_Launch
from models.Hello import Hello

class HelloWorld(webapp.RequestHandler):
	def get(self):
		self.post()
	def post(self):
		# Loads the LTI data/session
		launch = LTI_Launch(self)

		if launch.loaded:
			hello = Hello.getlist()
			env = jinja2.Environment('../views')
			template = env.get_template('hello.html')

			template_values = {
				'list' : hello,
			}

			html = template.render(template_values)
			self.response.out.write(html)
		else:
			self.response.out.write('Please load this page in LTI')
				
