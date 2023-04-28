from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    with open("rampe-treppe.json", "r") as file:
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

if __name__ == "__main__":
    app.run(debug=True)
