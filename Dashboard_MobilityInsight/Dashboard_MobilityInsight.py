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
# Version: v1.4.1
# ----------------------------------------------

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import dash_table

# Import von JSON
df = pd.read_json("rampe-treppe.json")
dff = df.copy()
#print(df.columns)
#print(df)

# Filterung dff für fig1 und fig2
dff_fltrd1 = dff[(dff["b_jahr"] >= 1960) & (dff["b_jahr"] <= 2023)] # Filtern nach Baujahre zwischen 1960 und 2023

# Filterung dff für fig3
dff_fltrd2 = dff[(dff["b_jahr"] >= 1960) & (dff["b_jahr"] <= 2023)] # Filtern nach Baujahre zwischen 1960 und 2023
dff_fltrd2["steigung"] = pd.to_numeric(dff_fltrd2["steigung"], errors="coerce") # Konvertierung string to numeric data type & ungültige Werte werden durch NaN ersetzt
dff_fltrd2 = dff_fltrd2[dff_fltrd2["steigung"].notnull() & (dff_fltrd2["steigung"] % 1 == 0)] # Filtern nach Ganzen Zahlen (NaN und andere Werte werden ignoriert)
handlauf_values = ["einseitig", "beidseitig", "kein"] # Vorbereitung des Filterns nach spezifischen Werten in "handlauf"/Liste - siehe nächste Zeile
dff_fltrd2 = dff_fltrd2[dff_fltrd2["handlauf"].isin(handlauf_values)] # Filtern nach den Werten aus "handlauf_values"


# Anwendung erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Balkendiagramm 1 (fig1): Diagramm

fig1 = px.histogram(dff_fltrd1, x="b_jahr",
             color='typ', barmode='group',
             # height=400
             )

# Balkendiagramm 1 (fig1): Layout
fig1.update_layout(
    barmode='group',
    font=dict(color='#FFFFFF'),
    title_text='Anzahl der Rampen und Treppen in Abhängigkeit vom Baujahr',
    xaxis_title="Baujahr",
    yaxis_title="Anzahl",
    legend=dict(title="Typ"),
    #plot_bgcolor='#064D5C',  # Farbe Innenbereich
    paper_bgcolor='#064D5C'   # Farbe Aussenbereich
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
fig2.update_layout(
    font=dict(color='#FFFFFF'),
    title='Durchschnittliche Breite und Länge von Treppen und Rampen', 
    xaxis_title='Baujahr',
    yaxis_title='Durchschnittliche Breite und Länge',
    paper_bgcolor='#064D5C'   # Farbe Aussenbereich
    )


# Balkendiagramm 2 (fig3): Diagramm

# Bins & Labels für Clustering
bins = [0, 5, 10, 15, 20]
labels = ["0-5%", "6-10%", "11-15%", "16-20%"]

# Neue Spalte "steigung_cluster" inkl. Labels
dff_fltrd2["steigung_cluster"] = pd.cut(dff_fltrd2["steigung"], bins=bins, labels=labels, include_lowest=True)

# Definition der korrekten Cluster-Reihenfolge im Diagramm - nach "labels"
category_orders = {"steigung_cluster": labels}

fig3 = px.histogram(dff_fltrd2, x="steigung_cluster", color="handlauf", barmode="group", category_orders=category_orders)

# Balkendiagramm 2 (fig3): Layout anpassen
fig3.update_layout(
    barmode='group',
    font=dict(color='#FFFFFF'),
    title_text='Anzahl der Zugänge nach Steigung und Handlaufpräsenz',
    xaxis_title="Steigung",
    yaxis_title="Anzahl Zugänge",
    legend=dict(title="Handlauftyp"),
    paper_bgcolor='#064D5C'   # Farbe Aussenbereich
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

df2 = pd.DataFrame(haltestellen)

fig4 = px.scatter_mapbox(df2, lat="lat", lon="lon", color="nutzung", size="nutzung",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=5)

fig4.update_layout(
    font=dict(color='#FFFFFF'),
    mapbox_style="open-street-map",
    title="Einfluss der Nähe von Sehenswürdigkeiten auf die Fahrgastnutzung",
    legend=dict(title="Nutzungsintensität"),
    paper_bgcolor='#064D5C',   # Farbe Aussenbereich
    height=600
    )


# Popup Fenster: Daten für die Tabelle
data = {'Name': ['\u2211 Attributwerte', '\u2211 Attribute', 'Attributnamen'], 'Wert': [131010, 30, 'anteil_eigentum, b_jahr, bauart...']}
df_table = pd.DataFrame(data)

# Layoutelemente für das Dashboard 
app.layout = html.Div(
    style={'background-color': '#064D5C'},
    children=[
    html.Div(style={'width': '60px', 'backgroundColor': 'black'}),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Img(src="/assets/logo2.svg", style={'height':'70px', 'width':'auto', 'margin-left':'20px', 'margin-top':'20px'}),
                    html.H1("Dashboard - Mobility Insight", style={'color': '#FFFFFF'}),
                    dbc.Button(
                        html.Img(src="/assets/info2.svg", style={'height':'30px', 'width':'auto'}), id="open", 
                        style={'background-color': '#FFFFFF', 'border-color': '#FFFFFF' }) # Verändert die Farbe des kompletten Buttons
                ],
                style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'background-color': '#064D5C'}
            ),
            html.Div(
                children=[
                    html.H3("Andrea Zimmermann · Irene Antolín Pérez · Philipp Michtner · Salvatore Russo · Sophie Pilz", style={'fontSize': '0.8em', 'textAlign': 'center', 'color': '#FFFFFF', 'background-color': '#064D5C', 'margin-bottom':'5px'}),
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
        dcc.Tab(label='Balken- und Liniendiagramme', children=[
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
        dcc.Tab(label='Karte', children=[
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
