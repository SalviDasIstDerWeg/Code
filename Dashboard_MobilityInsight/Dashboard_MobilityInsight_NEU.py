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
# Aufgabe: Finales Dashboard (Dashboard erstellen)
# Abgabedatum: 01.07.2023
# Version: NEU (w/ Data Import) - v1.2
# ----------------------------------------------

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import dash_table

#Import von JSON
df = pd.read_json("rampe-treppe.json")
dff = df.copy()
#print(df.columns)
#print(df)

#Filterung des dff für fig1 und fig2
dff_fltrd1 = dff[(dff["b_jahr"] >= 1960) & (dff['b_jahr'] <= 2023)]

# Anwendung erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Balkendiagramm 1 (fig1): Diagramm

fig1 = px.histogram(dff_fltrd1, x="b_jahr",
             color='typ', barmode='group',
             height=400)

# Balkendiagramm 1 (fig1): Layout
fig1.update_layout(
    barmode='group',
    title_text='Anzahl der Rampen und Treppen in Abhängigkeit vom Baujahr',
    xaxis_title="Baujahr",
    yaxis_title="Anzahl",
    #paper_bgcolor='rgba(240, 240, 240, 0.5)',  # Farbe Aussenbereich hellgrau
    #plot_bgcolor='rgba(240, 240, 240, 0.5)'   # Farbe Innenbereich hellgrau
)


# Liniendiagramm (fig2): Diagramm

#Nach Jahr gruppierter Datensatz - as_index=False, da die Spalte b_jahr weiterhin als Spalte verfügbar sein soll
dff_group = dff_fltrd1.groupby(['b_jahr'], as_index=False)[['breite', 'lange_m']].mean()
#print(df_group)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=dff_group["b_jahr"], y=dff_group["breite"],
                    mode='lines',
                    name='Breite'))

fig2.add_trace(go.Scatter(x=dff_group["b_jahr"], y=dff_group["lange_m"],
                    mode='lines',
                    name='Länge'))

# Liniendiagramm (fig2): Achsenbeschriftungen und Titel hinzufügen
fig2.update_layout(title='Entwicklung der durchschnittlichen Breite und Länge von Treppen und Rampen', 
                   xaxis_title='Baujahr', yaxis_title='Durchschnittliche Breite und Länge')


# Balkendiagramm 2 (fig3): Daten 
steigung_kategorien = ['0-5%', '6-10%', '11-15%', '16-20%']
zugänge_mit_handlauf = [25, 15, 10, 5]
zugänge_ohne_handlauf = [5, 10, 15, 20]

# Balkendiagramm 2 (fig3): Erstellung
fig3 = go.Figure(data=[
    go.Bar(name='Mit Handlauf', x=steigung_kategorien, y=zugänge_mit_handlauf),
    go.Bar(name='Ohne Handlauf', x=steigung_kategorien, y=zugänge_ohne_handlauf)
])

# Balkendiagramm 2 (fig3): Layout anpassen
fig3.update_layout(
    barmode='group',
    title_text='Anzahl der Zugänge nach Steigung und Handlaufpräsenz',
    xaxis_title="Steigung",
    yaxis_title="Anzahl Zugänge"
)


# Map (fig4): Daten
haltestellen = [
    {'name': 'Zürich HB', 'lat': 47.378177, 'lon': 8.540192, 'nutzung': 3000},
    {'name': 'Bern', 'lat': 46.948271, 'lon': 7.451451, 'nutzung': 2000},
    {'name': 'Genf', 'lat': 46.210759, 'lon': 6.142256, 'nutzung': 1500},
    {'name': 'Luzern', 'lat': 47.050168, 'lon': 8.309307, 'nutzung': 1000},
    {'name': 'Basel', 'lat': 47.559602, 'lon': 7.588576, 'nutzung': 2500},
    {'name': 'Lausanne', 'lat': 46.519962, 'lon': 6.633597, 'nutzung': 1200},
]

df = pd.DataFrame(haltestellen)

fig4 = px.scatter_mapbox(df, lat="lat", lon="lon", color="nutzung", size="nutzung",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=5)

fig4.update_layout(mapbox_style="open-street-map", title="Einfluss Nähe Sehenswürdigkeiten auf die Fahrgastnutzung")


# Popup Fenster: Daten für die Tabelle
data = {'Name': ['\u2211 Attributwerte', '\u2211 Attribute', 'Attributnamen'], 'Wert': [131010, 30, 'anteil_eigentum, b_jahr, bauart...']}
df_table = pd.DataFrame(data)

# Layoutelemente für das Dashboard 
app.layout = html.Div([
    html.Div(style={'width': '60px', 'backgroundColor': 'black'}),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Img(src="/assets/logo.svg", style={'height':'70px', 'width':'auto', 'margin-left':'20px', 'margin-top':'20px'}),
                    html.H1("Dashboard - Mobility Insight"),
                    dbc.Button(html.Img(src="/assets/info.svg", style={'height':'30px', 'width':'auto', 'margin-right':'20px'}), id="open")
                ],
                style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'}
            ),
            html.Div(
                children=[
                    html.H3("Andrea Zimmermann · Irene Antolín Pérez · Philipp Michtner · Salvatore Russo · Sophie Pilz", style={'fontSize': '0.8em', 'textAlign': 'center'}),
                ]
            )
        ]
    ),
     # Popup-Fenster
     dbc.Modal(
        [
            dbc.ModalHeader("Informationen zum Datensatz"),
            dbc.ModalBody([
                "Datenquelle: rampe-treppe.json",
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_table.columns],
                    data=df_table.to_dict('records'),
                ),
            ]),
            dbc.ModalFooter(
                dbc.Button("Schliessen", id="close", className="ml-auto")
            ),
        ],
        id="modal",
    ),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Balken- und Liniendiagramm', children=[
            html.Div([
                html.Div([
                    dcc.Graph(id='graph1', figure=fig1),
                    dcc.Graph(id='graph2', figure=fig2),
                ], style={'display': 'flex', 'justify-content': 'center'}),
                html.Div([
                    dcc.Graph(id='graph3', figure=fig3)
                ], style={'display': 'flex', 'justify-content': 'center'})
            ]),
        ]),
        dcc.Tab(label='Karte | Openstreetmap', children=[
            dcc.Graph(id='graph4', figure=fig4)
        ]),
    ]),
])

# Popup-Fenster: Interaktion
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
