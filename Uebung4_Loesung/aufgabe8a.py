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
# Aufgabenblatt 4, Aufgabe 8a
# Abgabedatum: 09.06.2023
# ----------------------------------------------

import math

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
from sklearn.datasets import make_blobs

# New: Density heatmap (2 columns) as third plot on tab 2
# with color and resolution options
# New: Everything with inline style and bootstrap (no CSS)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# generate random normal distributed data for x and y
# and store it in a Pandas DataFrame (for plot 1,2, and 5)

np.random.seed(seed=8)

df = pd.DataFrame({'y': np.random.normal(loc=0, scale=10, size=1000),
                   'x': np.random.normal(loc=10, scale=2, size=1000)})

# define cluster colors
COLORS = {'0': "red", '1': "blue", '2': "grey"}

# generic cluster data (for plot 3 and 4)
X, y = make_blobs(n_samples=7500, centers=3, n_features=2, random_state=0, cluster_std=0.75)

cluster_df = pd.DataFrame(data=X, columns=["X", "Y"])
cluster_df['cluster'] = [str(i) for i in y]

# Code NEU
app.layout = html.Div([
    html.H1("Dashboard - Aufgabe 8a"),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Tab One', children=[
            dbc.Row([
                dbc.Col([dcc.Dropdown(options=['red', 'green', 'blue'], value='red', id='color', multi=False)], width=6),
                dbc.Col([dcc.Slider(min=math.floor(df['y'].min()), max=math.ceil(df['y'].max()), id="min_value")], width=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="graph_1")],width=6),
                dbc.Col([dcc.Graph(id="graph_2")],width=6)
            ])
        ]),
        dcc.Tab(label='Tab Two', id="tab_2_graphs", children=[
            dbc.Row([
                dbc.Col([dcc.Graph(id="graph_3")], width=8),
                dbc.Col([dcc.Graph(id="graph_4")], width=4)
            ]),
            dbc.Row([
                dbc.Col(html.Div([
                    dbc.Label("Number of bins:", html_for="graph_5_nbins"),
                    dcc.Slider(id='graph_5_nbins', min=5, max=100, step=5, value=40)
                ]),width={"size": 3},),
                dbc.Col(html.Div([
                    dbc.Label("Color:", html_for="graph_5_color"),
                    dcc.Dropdown(options=["Viridis", "Magma", "Hot", "GnBu", "Greys"], value='Viridis', id='graph_5_color', multi=False)
                ]),width={"size": 3,"offset": 1},),
                dbc.Col(html.Div([
                    dbc.Label("Separated for Cluster:", html_for="graph_5_separated"),
                    dcc.RadioItems(options=["Yes","No"], value='No', id='graph_5_separated')
                ]),width={"size": 3,"offset": 1},),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="graph_5")], width=12)
            ])
        ]),
    ])
])
@app.callback(
    Output("graph_5", "figure"),
    Output("graph_3", "figure"),
    Output("graph_4", "figure"),
    Input("graph_5_nbins", "value"),
    Input("graph_5_color", "value"),
    Input("graph_5_separated", "value"),
)
def update_all_graphs(nbins, color, separated):
    fig5 = px.density_heatmap(cluster_df, x="X", y="Y", nbinsx=int(nbins), nbinsy=int(nbins), color_continuous_scale=color, facet_col=None if separated == "No" else "cluster",
        category_orders={"cluster": ["0", "1", "2"]})
    fig5.update_layout(template="plotly_white")
    
    fig3 = px.scatter(cluster_df, x="X", y="Y", color="cluster", color_discrete_map=COLORS, category_orders={"cluster": ["0", "1", "2"]})
    fig3.update_traces(marker=dict(size=8 * nbins / 40))  # Markergröße skaliert mit nbins
    fig3.update_layout(height=400, template="plotly_white", coloraxis_showscale=False)
    
    group_counts = cluster_df.sample(frac=nbins / 100)[['cluster', 'X']].groupby('cluster').count()  # Probenzahl skaliert mit nbins
    fig4 = go.Figure(data=[go.Bar(x=group_counts.index, y=group_counts['X'], marker_color=[COLORS.get(i) for i in group_counts.index])])
    fig4.update_layout(height=400, template="plotly_white", title="<b>Counts per cluster</b>", xaxis_title="cluster", title_font_size=25)
    
    return fig5, fig3, fig4
# Code NEU ENDE

@app.callback(Output("graph_1", "figure"), Input("color", "value"))
def update_graph_1(dropdown_value_color):
    fig = px.histogram(df, x="y", color_discrete_sequence=[dropdown_value_color])
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("graph_2", "figure"), Input("min_value", "value"))
def update_graph_2(min_value):
    if min_value:
        dff = df[df['y'] > min_value]
    else:
        dff = df

    fig = px.scatter(dff, x='x', y='y')
    fig.update_layout(template="plotly_white")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8014)
