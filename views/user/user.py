import flask
import sirope

from model.User import User


def get_blueprint():
    usr_module = flask.blueprints.Blueprint("user_blueprint", __name__,
                                            url_prefix="/user",
                                            template_folder="templates",
                                            static_folder="static")
    syrp = sirope.Sirope()
    return usr_module, syrp


user_blueprint, srp = get_blueprint()


@user_blueprint.route("/add", methods=["POST"])
def user_add(username=None, password=None):
    if username is None:
        username = flask.request.form.get("username", "").strip()
    if password is None:
        password = flask.request.form.get("password", "").strip()

    if (not username
            or not password):
        flask.flash("Faltan credenciales...")
        return flask.redirect("/")
    ...

    if User.find(srp, username):
        flask.flash("Pero... ¡si ya estás en el sistema!")
        return flask.redirect("/")
    ...

    usr = User(username, password)
    srp.save(usr)
    flask.flash("Ahora ya puedes entrar con tus nuevas credenciales.")
    return flask.redirect("/")
