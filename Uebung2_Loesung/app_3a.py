from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    # JSON-Datei öffnen und Daten laden
    with open("rampe-treppe.json", "r") as file:
        data = json.load(file)

    return render_template("index_3a.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
