# -----------------------------------------------
# Autoren:
# Philipp Michtner
# Salvatore Russo
# Sophie Pilz
#
# Institution: FHGR
# Kurs: Dashboard Design, MScUED&DV-WPF-FS23
# Aufgabenblatt 2, Aufgabe 3b
# Abgabedatum: 12.05.2023
# -----------------------------------------------

from flask import Flask, render_template, request

# Importiere JSON-Modul für Verarbeitung JSON-Dateien
import json
import os

# Erstelle Flask-Anwendung, Zuweisung der Variable "app"
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
   # Ermittle absoluten Pfad zur aktuellen Datei
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, 'rampe-treppe.json') # file_path für JSON-Datei
    
    # JSON-Datei öffnen und Daten laden
    with open(file_path, "r") as file:  # Verwendung von file_path
        data = json.load(file)

    bauart_options = sorted(set([item["bauart"] for item in data if item["bauart"] is not None]))
    b_jahr_options = sorted(set([item["b_jahr"] for item in data if item["b_jahr"] is not None]))

    if request.method == "POST":
        selected_bauart = request.form["bauart"]
        selected_b_jahr = request.form["b_jahr"]

        if selected_bauart:
            data = [item for item in data if item["bauart"] == selected_bauart]
        if selected_b_jahr:
            data = [item for item in data if item["b_jahr"] == selected_b_jahr]
    else:
        selected_bauart = ""
        selected_b_jahr = ""

    return render_template("index_3b.html", data=data, bauart_options=bauart_options, selected_bauart=selected_bauart, b_jahr_options=b_jahr_options, selected_b_jahr=selected_b_jahr)

# Wenn Python-Datei direkt ausgeührt wird, startet Flask-App im Debug-Modus
if __name__ == "__main__":
    app.run(debug=True)

