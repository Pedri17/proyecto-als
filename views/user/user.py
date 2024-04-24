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
def user_add():
    usr_email = flask.request.form.get("edEmail", "").strip()
    usr_passw = flask.request.form.get("edPswd", "").strip()

    if (not usr_email
            or not usr_passw):
        flask.flash("Faltan credenciales...")
        return flask.redirect("/")
    ...

    if User.find(srp, usr_email):
        flask.flash("Pero... ¡si ya estás en el sistema!")
        return flask.redirect("/")
    ...

    usr = User(usr_email, usr_passw)
    srp.save(usr)
    flask.flash("Ahora ya puedes entrar con tus nuevas credenciales.")
    return flask.redirect("/")