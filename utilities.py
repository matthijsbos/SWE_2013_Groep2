import flask

def render_template(template_name, **kwargs):
    """Wrapper for flask's render_template which also passes in some default
    variables (currently the lti object)."""

    kwargs['lti'] = flask.g.lti
    return flask.render_template(template_name, **kwargs)
