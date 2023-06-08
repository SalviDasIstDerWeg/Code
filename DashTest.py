from dash import Dash, dcc, html

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Hallo, Dash!"),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [{"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "Berlin"}],
                "layout": {"title": "Dash Bar Chart"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
