# -----------------------------------------------
# Autor:innen:
# Andrea Zimmermann
# Irene Antolín Pérez
# Philipp Michtner
# Salvatore Russo
# Sophie Pilz
#
# Institution: FHGR
# Kurs: Dashboard Design, MScUED&DV-WPF-FS23
# Aufgabenblatt 3, Aufgabe 6b
# Abgabedatum: 26.05.2023
# ----------------------------------------------

import math
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

# new: plotly template="plotly_white", https://plotly.com/python/templates/

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.DataFrame({'y': np.random.normal(loc=0, scale=10, size=1000), 'x': np.random.normal(loc=10, scale=2, size=1000), 'z': np.random.normal(loc=15, scale=2, size=1000)})

image = "https://media4.giphy.com/media/a93jwI0wkWTQs/giphy.gif"

app.layout = html.Div([html.Div([html.H1("Dashboard 3")], className="header"), html.Div([dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='Tab One', id="tab_1_graphs", children=[html.Div([
                dbc.Row([dbc.Col([dcc.Dropdown(options=['red','green','blue'], value='red', id='color', multi=False)], width=6),
                         dbc.Col([dcc.Slider(min=math.floor(df['y'].min()),max=math.ceil(df['y'].max()),id="min_value")], width=6)]),
                dbc.Row([dbc.Col([dcc.Graph(id="graph_1")],width=6),
                         dbc.Col([dcc.Graph(id="graph_2")],width=6)])], className="tab_content"),]),
            dcc.Tab(label='Tab Two', id="tab_2_graphs", children=[html.Div([
                #Tab Two content begins
                dbc.Row([dbc.Col([dcc.Dropdown(options=['pink','green','orange'], value='green', id='color_2', multi=False)], width=6),
                         dbc.Col([dcc.Dropdown(options=['purple','blue','red', 'green'], value='blue', id='color_3', multi=False)], width=6)]),
                dbc.Row([dbc.Col([dcc.Graph(id="graph_3")],width=6),
                         dbc.Col([dcc.Graph(id="graph_4")],width=6)])
                #Tab Two content ends
                ], className="tab_content"),]),
            dcc.Tab(label='Tab Three', id="tab_3_graphs", children=[html.Div([
                #Tab Three content begins
                dbc.Row([dbc.Col()],),
                         dbc.Col([html.Img(src=image, width="100%")], width=6)
                #Tab Three content ends
                ], className="tab_content")]),])], className="content")])

@app.callback(Output("graph_1", "figure"), Input("color", "value"))

def update_graph_1(dropdown_value_color):
    fig = px.histogram(df, x="y", color_discrete_sequence=[dropdown_value_color])
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("graph_2", "figure"),Input("min_value", "value"))

def update_graph_2(min_value):
    if min_value:
        dff = df[df['y'] > min_value]
    else:
        dff = df
    fig = px.scatter(dff, x='x', y='y')
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("graph_3", "figure"), Input("color_2", "value"))

def update_graph_3(dropdown_value_color):
    fig = px.line(df, x="y", y="x", color_discrete_sequence=[dropdown_value_color])
    fig.update_layout(template="plotly_dark")
    return fig

@app.callback(Output("graph_4", "figure"), Input("color_3", "value"))

def update_graph_4(dropdown_value_color):
    fig = px.scatter_matrix(df, dimensions=["x", "y", "z"], color_discrete_sequence=[dropdown_value_color])
    fig.update_layout(template="plotly_dark")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)