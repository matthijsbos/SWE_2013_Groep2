import flask
def render_template(template_name, **kwargs):
    print "test"
    kwargs['lti'] = flask.g.lti
    return flask.render_template(template_name, **kwargs)