import dash
from dash import html
from dash import dcc

from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as pex

pex.set_mapbox_access_token(open(".mapbox_token").read())
df = pd.read_csv('data.csv')
df = df.replace({'material':'aluminum'},'aluminium')
df = df.replace({'brand': [
    'plastic',
    'big plastic',
    'can',
    'cap',
    'candywrapper',
    'metal',
    'beer',
    'cup',
    'paper',
    'papercup',
    'aluminium',
    'aluminum',
    'plasticbottle',
    'bag',
    'foil',
    'packaging',
    'wrapper',
    'bottlecap',
    'chemicals']}, 'unknown' )
df = df.sort_values(by=['brand','material'])

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Dashboard'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in df['brand'].unique()],
        value='Breda'),
    dcc.Loading(
        dcc.Graph(
            id='location-graph',
            style={"height": 800}
        ),
        className="svg-container",
        style={"height": 250},
    )
])


@app.callback(
    Output(component_id='location-graph', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)

def update_graph(selected):
    filtered_data = df[df['brand'] == selected]
    fig = pex.scatter_mapbox(
        filtered_data,
        lat='lat',
        lon='lon',
        color = 'material',
        hover_name='material',
        zoom = 12,
        center = {"lon": df['lon'][0], "lat": df['lat'][0]},
        title = f'Trash Location of {selected}'
    )
    fig.update_layout(mapbox_style="open-street-map")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
