"""
Configuration file for the webapp.
"""

# Hosts the server binds itself to.
host = '0.0.0.0'

# Debug mode shows stacktraces etc. Disable for production server.
debug = True

# Key used for storing sessions. This should be something random.
secret_key = 'Hurdygurdy'

# The LTI consumers. Should be a different key/secret for every consumer (ie.
# for every Sakai, Blackboard, etc). Every line has a pair of key and secret.
# Both key and secret should always be surrounded by quotes!
consumers = {
    'sakai': 'secret',
    'blackboard': 'secret',
    'moodle': 'secret'
}
