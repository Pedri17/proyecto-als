import flask
import sirope

from model.User import User


def get_blueprint():
    login_module = flask.blueprints.Blueprint("login_blueprint", __name__,
                                              url_prefix="/login",
                                              template_folder="templates",
                                              static_folder="static")
    syrp = sirope.Sirope()
    return login_module, syrp


login_blueprint, srp = get_blueprint()


@login_blueprint.route("/")
def login():
    return flask.send_from_directory(login_blueprint.static_folder, "login.html")


@login_blueprint.route("/", methods=["POST"])
def answer():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    return ("<html><body>"
            + f"RESULTADO {username} y contraseña {password}"
            + "</body></html>")