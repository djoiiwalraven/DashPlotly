import dash
from dash import html
from dash import dcc

from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as pex

pex.set_mapbox_access_token("pk.eyJ1IjoicGVucXV3aW4iLCJhIjoiY2poYW5jYmozMDQ1bDNkczd1bWZkNWRyNSJ9.qD2OoEO4YJaQbcuEq4iL2g")
df = pd.read_csv('data.csv')

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Dashboard'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in df['brand'].unique()],
        value='Breda'),
    dcc.Graph(id='location-graph')
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
        zoom=1,
        title = f'Trash Location of {selected}'
    )
    fig.update_layout(mapbox_style="open-street-map")
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
