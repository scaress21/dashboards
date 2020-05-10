import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': 'rgb(228, 241, 245)',
    'text': 'rgb(44, 42, 87)'
}
#Importing data
mu = pd.read_csv('https://github.com/scaress21/dashboards/blob/master/museums/data/clean_museums.csv?raw=True')
state = pd.read_csv('https://github.com/scaress21/dashboards/blob/master/museums/data/museums_w_population.csv?raw=True')

#Choropleth Map
#Help from https://plotly.com/python/choropleth-maps/
state['text'] = 'Number of Museums: '+state['num_museums'].astype(str) + '<br>' + 'People per Museum: '+round(state['per_museum']).astype(str) +\
                 '<br>' +  'State: '+state['state']

data = go.Choropleth(autocolorscale = False, locations = state['code'], z = round(state['num_museums'].astype(int)), locationmode='USA-states', text = state['text'], colorscale= px.colors.sequential.Mint)

map = go.Figure(data)

map.update_layout(
title_text='Number of Museums in Each State',
geo = dict(
scope='usa',
projection=go.layout.geo.Projection(type = 'albers usa'),
showlakes=False)
)

#Setting up barchart
fig = make_subplots(rows=1, cols=2,
                    specs = [[{"type": "indicator"}, {"type": "pie"}]],)

fig.add_trace(go.Indicator(mode = "number",
                        value = 33006,
                        title = {"text": "Total Museums in the US"}
                ), row=1, col=1)

museum_types = ['Arboretum, Botanical Garden, or Nature Center', 'Art Museum', 'Children\s Museum', 'General Museum', 'Historic Preservation', 'History Museum', 'Natual History Museum', 'Science and Technology Museum or Planetarium', 'Zoo, Aquarium, or Wildlife Conservation' ]
num_museums = [1482, 3234, 511, 8676, 14846, 2283, 342, 1077, 555]


fig.add_trace(go.Pie(labels = museum_types, values = num_museums, title = 'Types of Museums',
                marker = {'colors' : ["rgb(253, 253, 204)", "rgb(206, 236, 179)", "rgb(156, 219, 165)",
                           "rgb(111, 201, 163)", "rgb(86, 177, 163)", "rgb(76, 153, 160)", "rgb(68, 130, 155)", "rgb(62, 108, 150)", "rgb(62, 182, 143)"]}),
    row=1, col=2)

bar = px.bar(mu, y = list(mu.groupby('museum_type')[['museum_type', 'museum_id']].count()['museum_id']),
                    x = sorted(mu['museum_type'].unique()),
                    title = 'Types of Museums',
                    color_discrete_sequence = ['darkcyan'],
                    labels = {'x':'Type', 'y':'Number of Museums'}
                )

#Setting up the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children = [
    html.Img(src= 'https://github.com/scaress21/dashboards/blob/master/museums/assets/United%20states%20of%20Museums.png?raw=True', alt = 'Header Image',
    style={'textAlign': 'center'}),
    dcc.Graph(
        id = 'us-map',
        figure= map
    ),
    dcc.Graph(
        id = 'stats',
        figure= fig
    ),
    dcc.Graph(
        id = 'main-graph',
        figure= bar)

])


if __name__ == '__main__':
    app.run_server(debug=True)
