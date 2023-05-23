# -----------------------------------------------
# Autoren:
# Andrea Zimmermann
# Irene Antolín Pérez
# Philipp Michtner
# Salvatore Russo
# Sophie Pilz
#
# Institution: FHGR
# Kurs: Dashboard Design, MScUED&DV-WPF-FS23
# Aufgabenblatt 3, Aufgabe 5a
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

app.layout = html.Div([html.H1("Dashboard 2"),
    dbc.Row([dbc.Col([dcc.Dropdown(options=['red', 'green', 'blue'], value='red', id='color', multi=False)], width=6),
             dbc.Col([dcc.RangeSlider(min=math.floor(df['y'].min()), max=math.ceil(df['y'].max()), id="range_value",
                                      value=[math.floor(df['y'].min()), math.ceil(df['y'].max())])], width=6)
    ]),
    dbc.Row([dbc.Col([dcc.Graph(id="graph_1")], width=6),
             dbc.Col([dcc.Graph(id="graph_2")], width=6)
    ])], className="m-4")

@app.callback(Output("graph_1", "figure"), Input("color", "value"))

def update_graph_1(dropdown_value_color):
    fig = px.histogram(df, x="y", color_discrete_sequence=[dropdown_value_color])
    fig.update_layout()
    return fig

@app.callback(Output("graph_2", "figure"), Input("range_value", "value"))

def update_graph_2(range_value):
    min_value, max_value = range_value
    dff = df[(df['y'] > min_value) & (df['y'] < max_value)]
    fig = px.scatter(dff, x='x', y='y')
    fig.update_layout()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
