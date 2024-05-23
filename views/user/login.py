import flask
import flask_login
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
    return flask.render_template("login.html")


@login_blueprint.route("/", methods=["POST"])
def answer():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    buttonAction = flask.request.form["buttonAction"]

    if buttonAction == "login":
        if User.current():
            flask_login.logout_user()
            flask.flash("Error inesperado." "login")
            return flask.redirect("/")
        ...

        if (not username
                or not password):
            flask.flash("Faltan credenciales", "login")
            return flask.redirect("/")
        ...

        usr = User.find(srp, username)

        if not usr:
            flask.flash("Usuario inexistente, revisa que está escrito correctamente", "login")
            return flask.redirect("/")
        if not usr.chk_password(password):
            flask.flash("Contraseña incorrecta, asegúrate de haberla escrito correctamente", "login")
            return flask.redirect("/")

        flask_login.login_user(usr)
        return flask.redirect("/")
    elif buttonAction == "register":
        return flask.redirect("/register")
