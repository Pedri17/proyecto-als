import flask_login
import sirope
import werkzeug.security as safe


class User(flask_login.mixins.UserMixin):
    def __init__(self, username, password):
        self._username = username
        self._password = safe.generate_password_hash(password)

    @property
    def username(self):
        return self._username

    def get_id(self):
        return self.username

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    @staticmethod
    def current():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr

    @staticmethod
    def find(srp: sirope.Sirope, username: str) -> "User":
        return srp.find_first(User, lambda u: u.username == username)
