# -----------------------------------------------
# Autor*innen:
# Andrea Zimmermann
# Irene Antolín Pérez
# Philipp Michtner
# Salvatore Russo
# Sophie Pilz
#
# Institution: FHGR
# Kurs: Dashboard Design, MScUED&DV-WPF-FS23
# Aufgabenblatt 3, Aufgabe 5b
# Abgabedatum: 26.05.2023
# ----------------------------------------------

import math
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# generate random normal distributed data for x and y
# and store it in a pandas DataFrame

df = pd.DataFrame({'y': np.random.normal(loc=0, scale=10, size=1000),
                   'x': np.random.normal(loc=10, scale=2, size=1000)})

# Tausch Reihenfolge Dropdown und Slider-Elemente
app.layout = html.Div([html.H1("Dashboard 2"),
    dbc.Row([
             dbc.Col([dcc.Slider(min=math.floor(df['y'].min()), max=math.ceil(df['y'].max()), id="min_value")], width=6),
             dbc.Col([dcc.Dropdown(options=[{'label': i, 'value': i} for i in ['red', 'green', 'blue']], value='red', id='color', multi=False)], width=6)
    ]),
    dbc.Row([dbc.Col([dcc.Graph(id="graph_1")], width=6),
             dbc.Col([dcc.Graph(id="graph_2")], width=6)
    ])], className="m-4")

# Callback Funktion graph_1 geändert, um auf Slider zu reagieren (nicht auf Dropdown)
@app.callback(Output("graph_1", "figure"), Input("min_value", "value"))
def update_graph_1(min_value):
    dff = df[df['y']> min_value]
    fig = px.histogram(dff, x="y")
    fig.update_layout()
    return fig

# Callback Funktion graph_2 geändert, um auf Dropdown zu reagieren (nicht auf Slider)
@app.callback(Output("graph_2", "figure"), Input("color", "value"))
def update_graph_2(dropdown_value_color):
    fig = px.scatter(df, x='x', y='y', color_discrete_sequence=[dropdown_value_color])
    fig.update_layout()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
