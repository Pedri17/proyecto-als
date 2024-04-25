import json

import flask
import flask_login
import sirope

from model.User import User

from views.user.user import user_blueprint
from views.user.login import login_blueprint


def create_app():
    flapp = flask.Flask(__name__)
    sirop = sirope.Sirope()
    login = flask_login.login_manager.LoginManager()

    flapp.config.from_file("instance/config.json", json.load)
    login.init_app(flapp)

    flapp.register_blueprint(user_blueprint)
    flapp.register_blueprint(login_blueprint)

    return flapp, sirop, login


app, srp, lm = create_app()


@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("unauthorized")
    return flask.redirect("/")


@lm.user_loader
def user_loader(username: str) -> User:
    return User.find(srp, username)


@app.route("/")
def main():
    usr = User.current()
    if usr is None:
        return flask.redirect("/login")
    else:
        return flask.redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)