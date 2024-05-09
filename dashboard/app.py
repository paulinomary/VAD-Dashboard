import dash
import dash_core_components as dcc
import dash_html_components as html
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css', 'styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(className='sidenav', children=[
        html.Div(className='sidenav-header', children=''),
        html.A('Home', href='/', className='active'),
    html.Nav(className='sidenav', children=[
        html.A(html.Img(src='./assets/components/Mini Logo branco.png', className='logo'), href='/'),
        html.A('Basic', href='basic'),
        html.A('Advanced', href='advanced'),
        html.A('About Us', href='about-us'),
    ]),
    html.Div(className='content',
             #Insert logo in the center of the page
             children=[
				 html.Img(src='./assets/components/Logo.png', className='center'),
				 html.H1('Welcome to our Dashboard'),
				 html.P('This is a simple dashboard example using Dash and Plotly.')
			 ])
])
])
if __name__ == '__main__':
    app.run_server(debug=True)