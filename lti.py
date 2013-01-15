import oauth.oauth as oauth
import flask

class LTIException(Exception):
    pass

class LTI_OAuthDataStore(oauth.OAuthDataStore):
    """Provides a data storage wrapper for OAuth.

    It handles the 'users' (consumers) of our LTI api. Each consumer has a
    'password' (secret)."""

    consumers = { 'sakai': 'secret' }

    def lookup_consumer(self, key):
        if key not in self.consumers:
            raise LTIException("Unknown consumer: %s" % key)
            return None

        return oauth.OAuthConsumer(key, self.consumers[key])

    # Some other functions that are not really used but have to be implemented.

    def lookup_token(self, token_type, token):
        return oauth.OAuthToken(None, None)

    def lookup_nonce(self, oauth_consumer, oauth_token, nonce):
        # Truste all nonces
        return None

class LTI():
    """Handles the authentification and storage of the LTI api.

    LTI uses OAuth for authentification. Then the LTI specific parameters are
    stored in a Flask session, for further requests."""

    def __init__(self, url, params, headers):
        """Starts or resumes the LTI session.

        The current page including the host should be passed for the value of
        url. The GET or POST parameters should be passed to params as a
        dictionary, and the headers should also be passed as a dictionary.

        The consumer name is automatically prepended to the user and course id
        to prevent collisions when using one app for multiple systems."""

        if "oauth_consumer_key" in params:
            # Start new session.

            oauth_server = oauth.OAuthServer(LTI_OAuthDataStore())
            oauth_server.add_signature_method(
                    oauth.OAuthSignatureMethod_PLAINTEXT())
            oauth_server.add_signature_method(
                    oauth.OAuthSignatureMethod_HMAC_SHA1())

            oauth_request = oauth.OAuthRequest.from_request("POST", url,
                    headers=headers, parameters=params)

            # verify_request needs token stuff... so we manually call the check.
            version = oauth_server._get_version(oauth_request)
            consumer = oauth_server._get_consumer(oauth_request)
            oauth_server._check_signature(oauth_request, consumer, None)

            flask.session['consumer'] = params['oauth_consumer_key']
            flask.session['user_id'] = params['user_id']
            flask.session['course_id'] = params['context_id']
            flask.session['course_name'] = params['context_title']
            flask.session['role'] = params['roles']
        else:
            # Resume old session, or error.
            if 'consumer' not in flask.session:
                raise LTIException("No OAuth-data and no session!")

    def destroy(self):
        session_data = ['consumer', 'user_id', 'course_id', 'course_name',
                'role']
        for s in session_data:
            flask.session.pop(s,  None)

    def get_consumer(self):
        return flask.session['consumer']

    def get_user_id(self):
        return "%s:%s" % (flask.session['consumer'], flask.session['user_id'])

    def get_course_id(self):
        return "%s:%s" % (flask.session['consumer'], flask.session['course_id'])

    def get_course_name(self):
        return flask.session['course_name']

    def is_instructor(self):
        return flask.session['role'] == "Instructor"

    def dump_all(self):
        ret = "<pre>"
        ret += "get_consumer = %s\n" % self.get_consumer()
        ret += "get_user_id = %s\n" % self.get_user_id()
        ret += "get_course_id = %s\n" % self.get_course_id()
        ret += "get_course_name = %s\n" % self.get_course_name()
        ret += "is_instructor = %s\n" % self.is_instructor()
        ret += "</pre>"
        return ret
