import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css', 'styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(className='sidenav', children=[
        html.Div(className='sidenav-header', children=''),
        html.A('Home', href='/', className='active'),
        html.A('Basic', href='basic'),
        html.A('Advanced', href='advanced'),
        html.A('About Us', href='about-us'),
    ]),
    html.Div(className='content', children=[
        html.H2('Content Area'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
