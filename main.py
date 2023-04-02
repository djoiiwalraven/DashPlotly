import dash
from dash import html
from dash import dcc
from dash import no_update
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as pex

import json

pex.set_mapbox_access_token(open(".mapbox_token").read())

# READING DATA
df = pd.read_excel('dataset.xlsm')

# CLEANING DATA
df = df.fillna('unknown')
df = df.replace({'material':['aluminum','metal']},'aluminium')
df = df.replace({'brand': [
    'plastic',
    'big plastic',
    'bisquitwrapper',
    'bottle',
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
df = df.replace({'brand':'autodrup'},'autodrop')
df = df.replace({'brand':'basicfitbreda'},'basic-fit')
df = df.replace({'brand':'btween'},'hero')
df = df.replace({'brand':'bueno'},'kinder')
df = df.replace({'brand':'bros'},'nestle')
df = df.sort_values(by=['brand','material'])

# CREATING DASH APP
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Dashboard'),
    dcc.Dropdown(
        id='dropdown',
        multi=False,
        options=[{'label': i, 'value': i} for i in df['brand'].unique()],
        value='7up'),
    dcc.Loading(
        dcc.Graph(
            id='location-graph',
            style={"height": 800},
            clear_on_unhover=True
        ),
        className="svg-container",
        style={"height": 250},
    ),
    dcc.Tooltip(id='graph-tooltip'),
    dcc.Store(id='filter_store'),
    #dcc.Store(id='select_store')
])

@app.callback(
    Output(component_id='filter_store', component_property='data'),
    Output(component_id='location-graph', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def update_graph(selected):
    filtered_data = df[df['brand'] == selected]
    fig = None
    fig = pex.scatter_mapbox(
        lat=filtered_data['lat'],
        lon=filtered_data['lon'],
        color = filtered_data['material'],
        zoom = 12,
        center = {"lon": df['lon'][0], "lat": df['lat'][0]},
        title = f'Trash Location of {selected}'
    )
    fig.update_traces(hoverinfo="none", hovertemplate=None)
    fig.update_layout(mapbox_style="open-street-map")
    
    # Dumb data into json to browser
    result = filtered_data.to_json(orient="records")
    parsed = json.loads(result)
    return parsed, fig

@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("location-graph", "hoverData"),
    Input(component_id='filter_store', component_property='data'),
)
def display_hover(hoverData,data):
    if hoverData is None:
        return False, no_update, no_update

    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]
    df_row = data[num]
    img_src = df_row['url']
    brand = df_row['brand']
    material = df_row['material']
    lat = df_row['lat']
    lon = df_row['lon']

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{brand}", style={"color": "darkblue", "overflow-wrap": "break-word"}),
            html.P(f"made of: {material}"),
            html.P(f"lat={lat}"),
            html.P(f"lon={lon}")
        ], style={'width': '200px', 'white-space': 'normal'})
    ]

    return True, bbox, children

if __name__ == '__main__':
    app.run_server(debug=True)
