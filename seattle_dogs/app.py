import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

all_pets = pd.read_csv('./data/clean_pet_data.csv')
dogs = pd.read_csv('./data/dog_breeds.csv')
cats = pd.read_csv('./data/cat_breeds.csv')

#First figure, barchart with dropdown
names = go.Figure()
names.add_trace(go.Bar(y = list(reversed(list(all_pets.groupby('name').count().sort_values('species', ascending = False)[:10].index))),
                      x = list(reversed(list(all_pets['name'].value_counts().sort_values(ascending = False)[:10]))),
                       name = 'Top Names for Pets',
                       marker = dict(color = 'rgb(255, 198, 196)'),
                      orientation = 'h'))

names.add_trace(go.Bar(y = list(reversed(list(all_pets[all_pets['species'] == 'Dog'].groupby('name').count().sort_values('species', ascending = False)[:10].index))),
                      x = list(reversed(list(all_pets[all_pets['species'] == 'Dog']['name'].value_counts().sort_values(ascending = False)[:10]))),
                       name = 'Top Names for Dogs',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)'),
                      orientation = 'h'))

names.add_trace(go.Bar(y = list(reversed(list(all_pets[all_pets['species'] == 'Cat'].groupby('name').count().sort_values('species', ascending = False)[:10].index))),
                      x = list(reversed(list(all_pets[all_pets['species'] == 'Cat']['name'].value_counts().sort_values(ascending = False)[:10]))),
                       name = 'Top Names for Cats',
                       visible = False,
                       marker = dict(color = 'rgb(227, 129, 145)'),
                      orientation = 'h'))

names.update_layout(
    updatemenus = [
      dict(
         active = 0,
          buttons = list([
             dict(label = 'All',
                  method = 'update',
                 args = [{'visible': [True, False, False]},
                          {'title' : 'Top Names for Pets'}]),
             dict(label = 'Dogs',
                  method = 'update',
                 args = [{'visible': [False, True, False]},
                          {'title' : 'Top Names for Dogs'}]),
             dict(label = 'Cats',
                  method = 'update',
                 args = [{'visible': [False, False, True]},
                          {'title' : 'Top Names for Cats'}]),

         ]),
            direction="down",
            pad={"r": 20, "t": 10},
            showactive=False,)
  ]),


names.update_layout(
    title_text="Top Names for Pets",
    showlegend=False,
    autosize=False,
    title_x=0.5,
    width=1000,
    height=400,
    paper_bgcolor= 'snow',
    margin=dict(
        l=50,
        r=50,
        b=20,
        t=100,
        pad=4
    ),
)
#Pie pie graph
pet_type = ['Dogs', 'Cats']
num = [33078, 15824]
col = ['rgb(139, 48, 88)', 'rgb(227, 129, 145)']

fig = make_subplots(rows = 3, cols = 2,
                    specs=[[{'type' : 'indicator'}, {'type':'pie','rowspan' : 3}],
                           [ {'type' : 'indicator'}, None],
                           [ {'type' : 'indicator'}, None] ],
                    subplot_titles=("", "Dogs vs Cats", "", ""))

fig.add_trace(go.Pie(labels = pet_type, values = num,
                       marker = dict(colors = col)), row = 1, col = 2)

fig.add_trace(go.Indicator(mode = "number",
                        value = 48941,
                        title = {"text": "Total Pets in Seattle"}
                ), row=1, col=1)
fig.add_trace(go.Indicator(mode = "number",
                        value = 40,
                        title = {"text": "New Licenses in 2020 So Far "}
                ), row=2, col=1)
fig.add_trace(go.Indicator(mode = "number",
                        value = 330,
                        title = {"text": "Breeds of Animals"}
                ), row=3, col=1)
fig.update_layout(height=600,
                  width = 1000,
                  showlegend=True,
                  paper_bgcolor= 'snow',
                  title_font_size=30,
                  margin=dict(
                      l=50,
                      r=50,
                      b=20,
                      t=100,
                      pad=4
                  ))

#Barchart of breeds
fig2 = make_subplots(rows = 1, cols = 2,
                    specs=[[{'type' : 'bar'}, {'type' : 'bar'}]],
                    subplot_titles=("Top Breeds of Cats", "Top Breeds of Dogs"),
                    horizontal_spacing = .08)
xdog = ['Retriever', 'Terrier', 'Labrador', 'Chihuahua', 'Short Coat', 'Golden', 'Poodle', 'Miniature', 'Spaniel', 'Australian Shepherd']
ydog = [6493, 4758, 4403, 1994, 1812, 1675, 1312, 1272, 1071, 1015]

xcat = list(reversed(['Russian Blue', 'Ragdoll', 'Maine Coon', 'LaPerm', 'Mix', 'Siamese', 'American Shorthair', 'Domestic Longhair', 'Domestic Medium Hair', 'Domestic Shorthair']))
ycat = list(reversed([127, 150, 250, 270, 294, 642, 923, 1191, 1916, 9184]))

fig2.add_trace(go.Bar(x = xdog, y = ydog,
                      marker = dict(color = 'rgb(244, 163, 168)')), row = 1, col = 2)
fig2.add_trace(go.Bar(x = xcat, y = ycat,
                      marker = dict(color = 'rgb(244, 163, 168)')), row = 1, col = 1)
fig2.update_layout(height=600,
                  width = 1000,
                  showlegend=False,
                  paper_bgcolor= 'snow',
                  margin=dict(
                      l=50,
                      r=50,
                      b=20,
                      t=100,
                      pad=4
                  ))
all_pets['issued'] = pd.to_datetime(all_pets['issued'])
all_pets['num'] = 1
#Line graphs
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2000].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2000].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2000',
                       visible = True,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2001].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2001].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2001',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2002].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2002].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2002',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2003].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2003].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2003',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2004].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2004].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2004',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2005].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2005].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2005',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2006].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2006].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2006',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2007].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2007].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2007',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2008].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2008].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2008',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2009].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2009].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2009',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2010].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2010].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2010',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2011].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2011].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2011',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2012].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2012].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2012',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2013].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2013].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2013',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2014].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2014].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2014',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2015].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2015].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2015',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2016].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2016].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2016',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2017].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2017].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2017',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2018].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2018].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2018',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2019].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2019].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2019',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))

fig3.add_trace(go.Scatter(x=all_pets[all_pets['issued'].dt.year == 2020].sort_values('issued')['issued'],
                        y= all_pets[all_pets['issued'].dt.year == 2020].sort_values('issued')['num'].cumsum(),
                       name = 'New Pet Licenses 2020',
                       visible = False,
                       marker = dict(color = 'rgb(139, 48, 88)')))
fig3.update_layout(
    updatemenus = [
      dict(
         active = 0,
          buttons = list([
              dict(label = '2000',
                  method = 'update',
                 args = [{'visible': [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2000'}]),
            dict(label = '2001',
                  method = 'update',
                 args = [{'visible': [False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2001'}]),
            dict(label = '2002',
                  method = 'update',
                 args = [{'visible': [False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2002'}]),
            dict(label = '2003',
                  method = 'update',
                 args = [{'visible': [False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2003'}]),
            dict(label = '2004',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2004'}]),
            dict(label = '2005',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2005'}]),
            dict(label = '2006',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2006'}]),
            dict(label = '2007',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2007'}]),
            dict(label = '2008',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2008'}]),
            dict(label = '2009',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2009'}]),
            dict(label = '2010',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2010'}]),
            dict(label = '2011',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2011'}]),
            dict(label = '2012',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2012'}]),
            dict(label = '2013',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2013'}]),
            dict(label = '2014',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2014'}]),
            dict(label = '2015',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False]},
                          {'title' : 'New Pet Licenses 2015'}]),
            dict(label = '2016',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False]},
                          {'title' : 'New Pet Licenses 2016'}]),
            dict(label = '2017',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False]},
                          {'title' : 'New Pet Licenses 2017'}]),
            dict(label = '2018',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]},
                          {'title' : 'New Pet Licenses 2018'}]),
            dict(label = '2019',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]},
                          {'title' : 'New Pet Licenses 2019'}]),
            dict(label = '2020',
                  method = 'update',
                 args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]},
                          {'title' : 'New Pet Licenses 2020'}]),

         ]),
            direction="down",
            pad={"r": 20, "t": 10},
            showactive=False,)
  ]),


fig3.update_layout(
    showlegend=False,
    autosize=False,
    width=1000,
    height=400,
    paper_bgcolor= 'snow',
    title_x=0.5,
    title_text="New Pet Licenses"
)



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(style={'backgroundColor': 'snow', 'textAlign' : 'center'}, children = [
    html.Img(src= 'https://github.com/scaress21/dashboards/blob/master/museums/assets/header_image.png?raw=True', alt = 'Header Image',
    style={
                'height': '50%',
                'width': '50%',
                'display': 'inline-block', 'vertical-align': 'middle'
            }
    ),
    dcc.Graph(
        id = 'names',
        figure= names
    ),
    dcc.Graph(
        id = 'stats',
        figure= fig
    ),
    dcc.Graph(
        id = 'main-graph',
        figure= fig2),
    dcc.Graph(
        id = 'line-graph',
        figure= fig3)

])
if __name__ == '__main__':
    app.run_server(debug=True)
