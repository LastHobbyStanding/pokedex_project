from flask import Flask, render_template, request, redirect, url_for
from pokedex import analyse_pokemon  # Your Python logic

app = Flask(__name__)

import os
port = int(os.environ.get("PORT", 10000))


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for('index'))  # Redirect to your home page

    query = request.form["query"]  # Pokémon name or number
    move_type = request.form.get("move_type", None)  # default to None
    result = analyse_pokemon(query, move_type)  # Pass both to logic
    return render_template("index.html", result=result)

@app.route("/defend", methods=["POST"])
def defend():
    query = request.form["query"]
    move_type = request.form["move_type"]
    result = analyse_pokemon(query, move_type)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

