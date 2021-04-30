import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import temperature_pd
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import math

# TODO - Use trigger to update data periodically

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)
app.title = "Temp Monitor"
server = app.server

common_layout = {
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    "yaxis": {
        "showgrid": False,
        "tickmode": "array",
        "title_text": None,
        "zeroline": False,
        "fixedrange": True,
        "tickfont": {"size": 20}
    },
    "xaxis": {
	"nticks": 3,
        "showgrid": False,
        "title_text": None,
        "zeroline": False,
        "fixedrange": True,
        "tickformat": "%e<br>%I:%M<br>%p",        
    },
    "showlegend": False,
    "margin": {"l":4,"r":4,"t":0, "b":0, "pad": 4}    
}
config = {'displayModeBar': False}

temperature_fig = None
humditiy_fig = None


def update_data():
    global temperature_fig, humidity_fig
    conn = temperature_pd.connect_database()
    df = temperature_pd.data_today(conn)

    if df is not None:
        temp_max = df['temperature'].max()
        temp_min = df['temperature'].min()
        humidity_max = df['humidity'].max()
        humidity_min = df['humidity'].min()
        temperature_fig = px.line(x=df['time'], y=df['temperature'])
        humidity_fig = px.line(x=df['time'], y=df['humidity'])
        temperature_layout = {
            "yaxis": {
                "tickvals": [temp_min, temp_max], 
                "ticktext": [f"{temp_min}", f"{temp_max}"],
                },
        }
        humidity_layout = {
            "yaxis": {
                "tickvals": [math.floor(humidity_min), math.ceil(humidity_max)], 
                "ticktext": [f"{math.floor(humidity_min)}", f"{math.ceil(humidity_max)}"],
                },
        }
        temperature_fig.update_layout(temperature_layout)
        temperature_fig.update_layout(common_layout)
        temperature_fig.update_traces(line={"color":"black"})
        humidity_fig.update_layout(humidity_layout)
        humidity_fig.update_layout(common_layout)
        humidity_fig.update_traces(line={"color":"black"})
    else:
        temperature_fig = go.Figure()
        humidity_fig = go.Figure()
        temperature_layout = {
            "yaxis": {
                'showticklabels': False,
                },
            "xaxis": {
                'showticklabels': False,
                },
        }
        humidity_layout = {
            "yaxis": {
                'showticklabels': False,
                },
            "xaxis": {
                'showticklabels': False,
                },
        }
        temperature_fig.update_layout(common_layout)
        humidity_fig.update_layout(common_layout)
        temperature_fig.update_layout(temperature_layout)
        humidity_fig.update_layout(humidity_layout)


def serve_layout():
    global temperature_fig, humidity_fig
    update_data()
    layout = dbc.Container(
        children=[
            dbc.Row(children=[
                    dbc.Col(
                            html.Img(
                                src="assets/logo.png",
                                style={
                                    "max-height": "2em",
                                },
                            ),
                        xs="6"
                        ),
                    dbc.Col(
                            html.H2(
                                f"{datetime.now().strftime('%B %d')}",
                                className="text-right text-bottom mb-0",
                            ),
                        xs="6"
                        ),
                ],
                style={"padding": "3em 1em", "height": "20vh"},
                justify="between",
                no_gutters=True,
            ),
            dbc.Row(children=[
                        html.Div(
                            dbc.Card(
                                dbc.CardBody(children=[
                                    dcc.Graph(figure = temperature_fig, config=config, style={"height": "100%"}),
                                    html.P("°C", style={
                                        "position":"absolute", "font-size":"1.7em", "right":"0.3em", "top": "0em",
                                        "color": "#323841ff",
                                        })
                                    ]
                                ),
                                style={
                                    "background": "linear-gradient(60deg, rgba(249,249,249,0.5), rgba(249,249,249,1))",
                                    "border-radius": "2em 0em 2em 2em",
                                    "height" : "100%",
                                },
                            ),
                            style={"padding": "0 1em 1em 1em", "margin": "0", "width":"100%", "height": "50%"}
                        ),
                        html.Div(
                            dbc.Card(
                                dbc.CardBody(children=[
                                    dcc.Graph(figure = humidity_fig, config=config, style={"height": "100%"}),
                                    html.P("%", style={
                                        "position":"absolute", "font-size":"1.7em", "right":"0.3em", "top": "0em",
                                        "color": "#323841ff",
                                        })
                                    ]
                                ),
                                style={
                                    "background": "linear-gradient(60deg, rgba(249,249,249,0.5), rgba(249,249,249,1))",
                                    "border-radius": "2em 0em 2em 2em",
                                    "height": "100%",
                                }
                            ),
                            style={"padding": "0 1em 1em 1em", "margin": "0", "width":"100%", "height": "50%"}
                        ),
                ],
                no_gutters=True,
                style={"height": "70vh"}
            ),
        ],
        style={
            "background-image": "linear-gradient(#939dac, #d5e5ff)",
            "height": "100vh",
            "padding": "0",
            },
        fluid=True
    )
    return layout

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
