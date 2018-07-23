# Wraps user for Flask_Login
from flask_login._compat import unicode


class dbUser(object):
    def __init__(self, user):
        self._user = user

    def get_id(self):
        return unicode(self._user.id)

    def is_active(self):
        return self._user.enabled

    def is_anonymouse(self):
        return False

    def is_authenticated(self):
        return True