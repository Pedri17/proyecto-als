import flask
import sirope

from model.User import User
from views.user.user import user_add


def get_blueprint():
    register_module = flask.blueprints.Blueprint("register_blueprint", __name__,
                                                 url_prefix="/register",
                                                 template_folder="templates",
                                                 static_folder="static")
    syrp = sirope.Sirope()
    return register_module, syrp


register_blueprint, srp = get_blueprint()


@register_blueprint.route("/")
def register():
    return flask.render_template("register.html")


@register_blueprint.route("/", methods=["POST"])
def answer():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    password_repeat = flask.request.form["password_repeat"]
    buttonAction = flask.request.form["buttonAction"]

    if buttonAction == "register":
        if password == password_repeat:
            user_add(username, password)
            return flask.redirect("/login")
        else:
            flask.flash("La contraseñas no coinciden", "password")
            return flask.redirect("/register")
    elif buttonAction == "return":
        return flask.redirect("/")
