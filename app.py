import flask

app = flask.Flask(__name__)


@app.route("/")
def get_index():
    return flask.send_from_directory(app.static_folder, "index.html")


@app.route("/hi", methods=["POST"])
def post_answer():
    nombre = flask.request.form["nombre1"]
    values = {
        "nombre_persona": nombre
    }
    return flask.render_template("response.html", **values)


if __name__ == "__main__":
    app.run(debug=True)