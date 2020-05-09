import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#Importing data
mu = pd.read_csv('https://github.com/scaress21/dashboards/blob/master/museums/data/clean_museums.csv?raw=True')
state = pd.read_csv('https://github.com/scaress21/dashboards/blob/master/museums/data/museums_w_population.csv?raw=True')

#Choropleth Map
state['text'] = 'Number of Museums: '+state['num_museums'].astype(str) + '<br>' + 'People per Museum: '+state['per_museum'].astype(str) +\
                'State: '+state['state']

data = go.Choropleth(autocolorscale = True, locations = state['state'], z = state['num_museums'].astype(int), locationmode='USA-states', text = state['text'])

map = go.Figure(data)

map.update_layout(
title_text='Number of Museums in Each State',
geo = dict(
scope='usa',
projection=go.layout.geo.Projection(type = 'albers usa'),
showlakes=False)
)

#Setting up traces
trace1 = go.Bar(y = list(mu.groupby('museum_type')[['museum_type', 'museum_id']].count()['museum_id']),
                    x = sorted(mu['museum_type'].unique()),
                    name = 'All States',
                )


#Setting up the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children = [
    html.H1(children='US Museums'),
    html.Div(children = '''Exploring US Museums by State'''),
    dcc.Graph(
        id = 'us-map',
        figure= map
    ),
    dcc.Graph(
        id = 'main-graph',
        figure={
            'data':[trace1],
            'layout': go.Layout(title='Museums by Category'),
        })

])


if __name__ == '__main__':
    app.run_server(debug=True)
