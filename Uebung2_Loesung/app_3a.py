# Importiere Flask-Klasse und render_template-Funktion aus der Flask-Bibliothek
# Flask: Web-Framework zur Erstellung von Webanwendungen
# render_template: Funktion zum Rendern von HTML-Dateien mit dynamischen Daten (Jinja2-Template-System)
from flask import Flask, render_template

# Importiere JSON-Modul zur Verarbeitung von JSON-Dateien
import json
import os

# Erstelle Flask-Anwendung und Zuweisung der Variable "app" , __name__ gibt Namen des aktuellen Moduls an
app = Flask(__name__)


# Pfaddefinition für index_xy
@app.route("/")
def index():
    # Ermittle den absoluten Pfad zur aktuellen Datei
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, 'rampe-treppe.json')
    
    # JSON-Datei öffnen und Daten laden
    with open(file_path, "r") as file:
        data = json.load(file)

    return render_template("index_3a.html", data=data)

# Wenn Python-Datei direkt ausgeührt wird, startet Flask-App im Debug-Modus
if __name__ == "__main__":
    app.run(debug=True)

