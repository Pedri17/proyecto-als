import flask
import sirope

from model.Folder import Folder
from model.User import User
from model.Note import Note


def get_blueprint():
    note_module = flask.blueprints.Blueprint("note_blueprint", __name__,
                                             url_prefix="/note",
                                             template_folder="templates",
                                             static_folder="static")
    syrp = sirope.Sirope()
    return note_module, syrp


note_blueprint, srp = get_blueprint()


@note_blueprint.route("/")
def note():
    folders = Folder.get_all_folders(srp, User.current())
    for thisFolder in folders:
        for i in range(len(thisFolder.notas)):
            if isinstance(thisFolder.notas[i], sirope.OID):
                thisFolder.notas[i] = Note.find(srp, thisFolder.notas[i])

    sust = {
        "notes": Note.get_all_notes(srp, User.current()),
        "folders": folders
    }

    return flask.render_template("noteMenu.html", **sust)


@note_blueprint.route("/", methods=["POST"])
def answer():
    buttonAction = flask.request.form["buttonNotes"]

    if len(buttonAction.split("/")) >= 3:
        thisOID = buttonAction.split("/")[1]
        thisAction = buttonAction.split("/")[2]
        return flask.redirect("/folder/"+srp.safe_from_oid(sirope.OID.from_text(thisOID)) + "/" + thisAction)

    if buttonAction == "newNote":
        return flask.redirect("/note/add")
    elif buttonAction == "newFolder":
        return flask.redirect("/folder/add")
    else:
        thisOID = buttonAction.split("/")[0]
        thisAction = buttonAction.split("/")[1]
        return flask.redirect(srp.safe_from_oid(sirope.OID.from_text(thisOID)) + "/" + thisAction)


@note_blueprint.route("/add")
def newNoteForm():
    sust = {
        "allFolders": srp.load_all(Folder)
    }
    return flask.render_template("note.html", **sust)


@note_blueprint.route("/add", methods=["POST"])
def createNote():
    titulo = flask.request.form["title"]
    contenido = flask.request.form["content"]
    buttonAction = flask.request.form["buttonAction"]
    newFolderStrOID = flask.request.form["selectFolder"]

    if buttonAction == "create":
        newNote = Note(titulo, contenido, User.current().username, [])
        oid = srp.save(newNote)
        if newFolderStrOID is not None and newFolderStrOID != "None":
            newFolder = Folder.find(srp, sirope.OID.from_text(newFolderStrOID))
            newFolder.notas.append(oid)
            srp.save(newFolder)

        return flask.redirect("/note")
    elif buttonAction == "return":
        return flask.redirect("/note")


@note_blueprint.route("/<string:id>/delete")
def deleteNote(id):
    noteOID = srp.oid_from_safe(id)
    noteToDelete = Note.find(srp, noteOID)
    Folder.delete_note_from_folders(srp, noteOID)
    srp.delete(noteOID)
    return flask.redirect("/note/")


@note_blueprint.route("/<string:id>/edit")
def editNoteForm(id):
    thisNote = Note.find(srp, srp.oid_from_safe(id))
    users = []
    for thisUser in thisNote.editores:
        users.append(str(thisUser))

    sust = {
        "allFolders": srp.load_all(Folder),
        "actualNote": srp.oid_from_safe(id),
        "titulo": thisNote.titulo,
        "contenido": thisNote.contenido,
        "users": users
    }
    return flask.render_template("editNote.html", **sust)


@note_blueprint.route("/<string:id>/edit", methods=["POST"])
def editNote(id):
    titulo = flask.request.form["title"]
    contenido = flask.request.form["content"]
    buttonAction = flask.request.form["buttonAction"]
    newFolderStrOID = flask.request.form["selectFolder"]
    usernames = flask.request.form.getlist("username_from_selector")

    if buttonAction == "edit":
        noteOID = srp.oid_from_safe(id)
        noteToEdit = Note.find(srp, noteOID)
        noteToEdit.titulo = titulo
        noteToEdit.contenido = contenido
        noteToEdit.creador = User.current().username
        noteToEdit.editores = usernames
        srp.save(noteToEdit)

        if newFolderStrOID is not None and newFolderStrOID != "None":
            Folder.delete_note_from_folders(srp, noteOID)
            newFolder = Folder.find(srp, sirope.OID.from_text(newFolderStrOID))
            newFolder.notas.append(noteToEdit.get_id())
            srp.save(newFolder)

        return flask.redirect("/note")
    elif buttonAction == "return":
        return flask.redirect("/note")


@note_blueprint.route("/<string:id>/see")
def seeNoteForm(id):
    thisNote = Note.find(srp, srp.oid_from_safe(id))

    sust = {
        "titulo": thisNote.titulo,
        "contenido": thisNote.contenido
    }
    return flask.render_template("seeNote.html", **sust)


@note_blueprint.route("/<string:id>/see", methods=["POST"])
def seeNote(id):
    return flask.redirect("/note")
