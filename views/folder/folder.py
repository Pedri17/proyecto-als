import flask
import sirope

from model.Folder import Folder
from model.User import User
from model.Note import Note


def get_blueprint():
    folder_module = flask.blueprints.Blueprint("folder_blueprint", __name__,
                                               url_prefix="/folder",
                                               template_folder="templates",
                                               static_folder="static")
    syrp = sirope.Sirope()
    return folder_module, syrp


folder_blueprint, srp = get_blueprint()


@folder_blueprint.route("/add")
def folder():
    return flask.render_template("folder.html")


@folder_blueprint.route("/add", methods=["POST"])
def answer():
    buttonAction = flask.request.form["buttonAction"]
    nombre = flask.request.form["title"]
    usernames = flask.request.form.getlist("username_from_selector")

    if buttonAction == "create":
        if User.current().username not in usernames:
            usernames.append(User.current().username)
        newFolder = Folder(nombre, [], usernames)
        srp.save(newFolder)
        return flask.redirect("/")
    else:
        return flask.redirect("/")


@folder_blueprint.route("/<string:id>/edit")
def editFolderForm(id):
    thisFolder = Folder.find(srp, srp.oid_from_safe(id))

    sust = {
        "users": thisFolder.usuarios,
        "actualName": thisFolder.nombre
    }

    return flask.render_template("editFolder.html", **sust)


@folder_blueprint.route("/<string:id>/edit", methods=["POST"])
def editFolder(id):
    buttonAction = flask.request.form["buttonAction"]
    nombre = flask.request.form["title"]
    usernames = flask.request.form.getlist("username_from_selector")

    if buttonAction == "edit":
        folderOID = srp.oid_from_safe(id)
        folderToEdit = Folder.find(srp, folderOID)
        folderToEdit.nombre = nombre
        folderToEdit.usuarios = usernames
        srp.save(folderToEdit)
        return flask.redirect("/")
    elif buttonAction == "return":
        return flask.redirect("/note")
    else:
        return flask.redirect("/")


@folder_blueprint.route("/<string:id>/delete")
def deleteFolder(id):
    srp.delete(srp.oid_from_safe(id))
    return flask.redirect("/note/")
